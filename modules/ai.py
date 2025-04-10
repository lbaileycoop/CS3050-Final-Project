"""Module that contains the definition for an AI object
as well as the methods for maintaining cross-check-sets"""

from .config import ROWS, COLS
from .board import Board, EMPTY_TILES, CROSS_CHECKS_ACROSS, CROSS_CHECKS_DOWN
from .tile import Tile
from .utils import (
    tiles_to_str,
    find_permutations_recursive,
    copy_list,
)
from .player import Player
from .drawbag import Drawbag


class AI(Player):
    """
    Class representing the AI

    Attributes:
        board (Board): Contains the Board that the AI exists within
        testing_board (list(list(Tile))): Contains a copy of the board that
            the AI uses to test moves on
        curr_cross_checks (list(list(set(str)))): Contains the cross check sets
            for the current direction the AI is traversing while it searches
    """

    def __init__(self, name: str, drawbag: Drawbag, board: Board):
        super().__init__(name, drawbag)
        self.board = board
        self.testing_board = []
        self.curr_cross_checks = []

    def find_moves(
        self,
    ) -> list[list[tuple[Tile, tuple[int, int]]]]:
        """
        Assembles a list of all possible moves
        (optimistic, moves not verified yet)
        """
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
        """
        Finds all of the possible moves in the passed row

        Also works for columns when the board is transposed
        """
        possible_moves: list[list[tuple[Tile, tuple[int, int]]]] = []

        letters_in_row = tiles_to_str(
            tile for tile in self.testing_board[row] if tile not in EMPTY_TILES
        )

        possible_words = find_permutations_recursive(
            "".join(self.rack.get_rack_letters()) + letters_in_row, []
        )
        feasable_words = possible_words

        # if letters_in_row != "":
        #     for word in possible_words:
        #         for letter in letters_in_row:
        #             if letter in word:
        #                 feasable_words.append(word)
        # elif row == 7:
        #     feasable_words = possible_words

        for word in feasable_words:
            first_letter = word[0]

            for col in range(COLS - len(word)):
                tile = self.testing_board[row][col]

                if (
                    tile.letter == first_letter
                    and col + len(word) <= COLS
                    or tile in EMPTY_TILES
                ):
                    possible_moves += self.find_move(word, (row, col), [], [])

        return possible_moves

    def find_move(
        self,
        target: str,
        coords: tuple[int, int],
        curr_move: list[tuple[Tile, tuple[int, int]]],
        possible_moves: list[list[tuple[Tile, tuple[int, int]]]],
    ):
        """Recursives traverses the row to the right to try and construct the target"""

        remaining_rack = []

        for tile in self.rack.get_rack():
            if tile not in [move[0] for move in curr_move]:
                remaining_rack.append(tile)

        if target == "":
            if curr_move not in possible_moves:
                possible_moves.append(curr_move)
            return possible_moves

        if coords is None:
            return possible_moves

        square = self.testing_board[coords[0]][coords[1]]
        next_letter = target[0]
        curr_move = copy_list(curr_move)

        if square not in EMPTY_TILES:
            if square.letter == next_letter:
                return self.find_move(
                    target[1:],
                    self.next_coords(coords),
                    curr_move,
                    possible_moves,
                )
            return possible_moves

        if next_letter in self.curr_cross_checks[coords[0]][coords[1]]:
            for tile in remaining_rack.copy():
                if next_letter == tile.letter:
                    curr_move.append((tile, coords))
                    remaining_rack.remove(tile)
                    return self.find_move(
                        target[1:],
                        self.next_coords(coords),
                        curr_move,
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
        """
        Returns a transposed (swap rows and columns) version of the board
        """
        transposed_board = []

        for row in range(ROWS):
            transposed_board.append([])
            for col in range(COLS):
                transposed_board[row].append(self.board.get_board()[col][row])

        return transposed_board

    def choose_move(self):
        """Chooses the highest scoring valid move and plays it into current tile"""
        moves = self.find_moves()
        valid_moves = {}
        max_score = 0
        max_move = None
        for move in moves:
            is_valid, score = self.board.test_turn(move)
            if is_valid:
                if score not in valid_moves:
                    valid_moves[score] = []
                valid_moves[score].append(move)
                if score > max_score:
                    max_score = score
                    max_move = move

        for tile in max_move:
            self.rack.remove_tile(tile[0])
            self.board.update_tile(tile[1][0], tile[1][1], tile[0])
