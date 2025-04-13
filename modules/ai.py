"""Module that contains the definition for an AI object
as well as the methods for maintaining cross-check-sets"""

from .config import SIZE
from .board import Board, EMPTY_TILES, CROSS_CHECKS_ACROSS, CROSS_CHECKS_DOWN
from .tile import Tile
from .utils import (
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
        personality (int): Which algorithm the AI uses to choose a move
            0 = Most points
            1 = Most words
            2 = Most tiles
            3 = Longest word
    """

    def __init__(self, name: str, drawbag: Drawbag, board: Board, personality: int = 0):
        super().__init__(name, drawbag)
        self.board = board
        self.testing_board = []
        self.curr_cross_checks = []
        self.personality = personality

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

        for row in range(SIZE):
            if True in [
                self.is_anchor(self.testing_board, row, col) for col in range(SIZE)
            ]:
                possible_moves_across += self.moves_in_row(row)

        self.testing_board = self.transpose_board()
        self.curr_cross_checks = CROSS_CHECKS_DOWN

        for row in range(SIZE):
            if True in [
                self.is_anchor(self.testing_board, row, col) for col in range(SIZE)
            ]:
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

        letters_in_row = []
        letters_in_word = ""
        for tile in self.testing_board[row]:
            if tile not in EMPTY_TILES:
                letters_in_word += tile.letter
            else:
                if letters_in_word != "":
                    letters_in_row.append(letters_in_word)
                letters_in_word = ""

        possible_words = find_permutations_recursive(
            self.rack.get_rack_letters() + letters_in_row, []
        )

        for word in possible_words:
            first_letter = word[0]

            for col in range(SIZE - len(word)):
                tile = self.testing_board[row][col]

                if (
                    tile.letter == first_letter
                    and col + len(word) <= SIZE
                    or tile in EMPTY_TILES
                ):
                    possible_moves += self.find_move(
                        word, (row, col), [], [], self.get_rack_tiles()
                    )

        return possible_moves

    # suppress warning for too many parameters
    # pylint: disable=R0913,R0917
    def find_move(
        self,
        target: str,
        coords: tuple[int, int],
        curr_move: list[tuple[Tile, tuple[int, int]]],
        possible_moves: list[list[tuple[Tile, tuple[int, int]]]],
        remaining_rack: list[Tile],
    ):
        """Recursives traverses the row to the right to try and construct the target"""

        if target == "":
            if curr_move not in (possible_moves + []):
                possible_moves.append(curr_move)
            return possible_moves

        if coords is None:
            return possible_moves

        square = self.testing_board[coords[0]][coords[1]]
        next_letter = target[0]
        curr_move = copy_list(curr_move)
        remaining_rack = copy_list(remaining_rack)

        if square not in EMPTY_TILES:
            if square.letter == next_letter:
                return self.find_move(
                    target[1:],
                    self.next_coords(coords),
                    curr_move,
                    possible_moves,
                    remaining_rack,
                )
            return possible_moves

        if next_letter in self.curr_cross_checks[coords[0]][coords[1]]:
            for tile in remaining_rack.copy():
                if tile.letter in [next_letter, ""]:
                    if tile.letter == "":
                        new_tile = Tile.copy(tile)
                        new_tile.set_blank(next_letter)
                        curr_move.append((new_tile, coords))
                    else:
                        curr_move.append((tile, coords))
                    remaining_rack.remove(tile)
                    return self.find_move(
                        target[1:],
                        self.next_coords(coords),
                        curr_move,
                        possible_moves,
                        remaining_rack,
                    )
        return possible_moves

    def next_coords(self, coords: tuple[int, int]) -> tuple[int, int] | None:
        """
        Returns the coordinates of the next square in the row, or
        None if passed square is the end of the row
        """
        if coords[1] + 1 < SIZE:
            return (coords[0], coords[1] + 1)
        return None

    def transpose_board(self):
        """
        Returns a transposed (swap SIZE and columns) version of the board
        """
        transposed_board = []

        for row in range(SIZE):
            transposed_board.append([])
            for col in range(SIZE):
                transposed_board[row].append(self.board.get_board()[col][row])

        return transposed_board

    def choose_move(self):
        """
        Chooses the highest scoring valid move and plays it into current tile

        Returns True of False depending on if a valid move was found
        """
        moves = self.find_moves()
        valid_moves = {}
        max_score = 0
        max_words = 0
        max_tiles = 0
        max_word_len = 0
        chosen_moves = [None, None, None, None]
        for move in moves:
            is_valid, words = self.board.test_turn(move)

            if is_valid:
                score = sum(words.values())
                if score not in valid_moves:
                    valid_moves[score] = []
                valid_moves[score].append(move)

                if score > max_score:
                    max_score = score
                    chosen_moves[0] = move
                if len(words) > max_words:
                    max_words = len(words)
                    chosen_moves[1] = move
                if len(move) > max_tiles:
                    max_tiles = len(move)
                    chosen_moves[2] = move
                for word in words.keys():
                    if len(word) > max_word_len:
                        max_word_len = len(word)
                        chosen_moves[3] = move

        chosen_move = chosen_moves[self.personality]

        if chosen_move is None:
            return False

        for tile in chosen_move:
            if tile[0].value == 0:
                self.rack.remove_letter("")
            else:
                self.rack.remove_letter(tile[0].letter)
            self.board.update_tile(tile[1][0], tile[1][1], tile[0])
        return True

    def is_anchor(self, board: list[list[Tile]], row: int, col: int):
        """
        Returns whether the tile at row, col is an anchor tile
        (empty and adjacent to a non-empty tile, or the central tile)
        """
        if board[row][col] not in EMPTY_TILES:
            return False

        if -1 < row + 1 < SIZE:
            if board[row + 1][col] not in EMPTY_TILES:
                return True
        if -1 < row - 1 < SIZE:
            if board[row - 1][col] not in EMPTY_TILES:
                return True
        if -1 < col + 1 < SIZE:
            if board[row][col + 1] not in EMPTY_TILES:
                return True
        if -1 < col - 1 < SIZE:
            if board[row][col - 1] not in EMPTY_TILES:
                return True
        return (row, col) == (7, 7)
