"""Module that contains the definition for an AI object
as well as the methods for maintaining cross-check-sets"""

from .config import ROWS, COLS, ALPHABET
from .board import Board, EMPTY_TILES, CROSS_CHECKS_ACROSS, CROSS_CHECKS_DOWN
from .rack import Rack
from .tile import Tile
from .utils import (
    tiles_to_str,
    find_permutations_recursive,
    copy_list,
)


class AI:
    """TODO"""

    def __init__(self, board: Board, rack: Rack):
        self.board = board
        self.testing_board = []
        self.curr_cross_checks = []
        self.rack = rack

    def across_moves(
        self,
    ) -> list[list[tuple[Tile, tuple[int, int]]]]:
        possible_moves_across: list[list[tuple[Tile, tuple[int, int]]]] = []
        possible_moves_down: list[list[tuple[Tile, tuple[int, int]]]] = []

        self.testing_board = copy_list(self.board.get_board())
        self.curr_cross_checks = CROSS_CHECKS_ACROSS

        for row in range(len(self.testing_board)):
            possible_moves_across += self.moves_in_row(row)

        self.testing_board = self.transpose_board()
        self.curr_cross_checks = CROSS_CHECKS_DOWN

        for row in range(len(self.testing_board)):
            possible_moves_down += self.moves_in_row(row)

        for move in possible_moves_down:
            for i, tile in enumerate(move):
                move[i] = (tile[0], tile[1][::-1])
        return possible_moves_across + possible_moves_down

    def moves_in_row(self, row: int) -> list[list[tuple[Tile, tuple[int, int]]]]:
        possible_moves: list[list[tuple[Tile, tuple[int, int]]]] = []

        letters_in_row = tiles_to_str(
            tile for tile in self.testing_board[row] if tile not in EMPTY_TILES
        )

        possible_words = find_permutations_recursive(
            "".join(self.rack.get_rack_letters()) + letters_in_row, []
        )
        feasable_words = []

        if letters_in_row != "":
            for word in possible_words:
                for letter in letters_in_row:
                    if letter in word:
                        feasable_words.append(word)
        elif row == 7:
            feasable_words = possible_words

        for word in feasable_words:
            first_letter = word[0]

            for col in range(COLS - len(word)):
                tile = self.testing_board[row][col]

                if (
                    tile.letter == first_letter
                    and col + len(word) <= COLS
                    or tile in EMPTY_TILES
                ):
                    possible_moves += self.find_word(
                        word, (row, col), [], copy_list(self.rack.get_rack()), []
                    )

        return possible_moves

    def find_word(
        self,
        target: str,
        coords: tuple[int, int],
        curr: list[tuple[Tile, tuple[int, int]]],
        remaining_rack: list[Tile],
        possible_moves: list[list[tuple[Tile, tuple[int, int]]]],
    ):

        if target == "":
            if curr not in possible_moves:
                possible_moves.append(curr)
            return possible_moves

        if coords is None:
            return possible_moves

        square = self.testing_board[coords[0]][coords[1]]
        next_letter = target[0]
        remaining_rack = copy_list(remaining_rack)
        curr = copy_list(curr)

        if square not in EMPTY_TILES:
            if square.letter == next_letter:
                return self.find_word(
                    target[1:],
                    self.next_coords(coords),
                    curr,
                    remaining_rack,
                    possible_moves,
                )
            return possible_moves

        if next_letter in self.curr_cross_checks[coords[0]][coords[1]]:
            for tile in remaining_rack.copy():
                if next_letter == tile.letter:
                    curr.append((tile, coords))
                    remaining_rack.remove(tile)
                    return self.find_word(
                        target[1:],
                        self.next_coords(coords),
                        curr,
                        remaining_rack,
                        possible_moves,
                    )
        return possible_moves

    def next_coords(self, coords: tuple[int, int]) -> tuple[int, int] | None:
        """
        Returns the coordinates of the next square in the row, or
        None if passed square is the end of the row
        """
        if coords[1] + 1 < COLS:
            return (coords[0], coords[1] + 1)
        return None

    def transpose_board(self):
        transposed_board = []

        for row in range(ROWS):
            transposed_board.append([])
            for col in range(COLS):
                transposed_board[row].append(self.board.get_board()[col][row])

        return transposed_board
