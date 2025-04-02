
from .config import ROWS, COLS, DICTIONARY
from .board import Board, EMPTY_TILES
from .rack import Rack
from .tile import Tile
from .utils import valid_word, tiles_to_str


ALPHABET = {'a','b','c','d','e','f',
            'g','h','i','j','k','l',
            'm','n','o','p','q','r',
            's','t','u','v','v','w',
            'x','y','z'}

CROSS_CHECKS_ACROSS = [[ALPHABET for _ in range(COLS)] for _ in range(ROWS)]
CROSS_CHECKS_DOWN = [[ALPHABET for _ in range(ROWS)] for _ in range(COLS)]

class AI:
    def __init__(self, board: Board, rack: Rack):
        self.board = board
        self.rack = rack

    def update_cross_checks(self):
        """ Updates the cross-check lists whenever a move is played """
        words = self.board.find_words()

        for tile in self.board.get_current_turn_tiles():
            coords = tile.coords

            if self.board.get_current_turn_tiles()[0].coords[0] - self.board.get_current_turn_tiles()[-1].coords[0] == 0:
                across = True
            else:
                across = False

            if across:
                CROSS_CHECKS_ACROSS[coords[0]][coords[1]] = []
                
                if coords[0]-1 > -1:
                    CROSS_CHECKS_ACROSS[
                        coords[0]-1][coords[1]] = {letter for letter in ALPHABET 
                                                if valid_word(letter+
                                                                tiles_to_str(self.board.find_string(coords, 1, 0))[0])}
                if coords[0]+1 < ROWS:
                    CROSS_CHECKS_ACROSS[
                        coords[0]+1][coords[1]] = {letter for letter in ALPHABET
                                                if valid_word(tiles_to_str(self.board.find_string(coords, -1, 0))[::-1]+
                                                                letter)}
            
            if not across or len(self.board.get_current_turn_tiles()) == 1:
                CROSS_CHECKS_DOWN[coords[0]][coords[1]] = []
                
                if coords[1]-1 > -1:
                    CROSS_CHECKS_DOWN[
                        coords[0]][coords[1]-1] = {letter for letter in ALPHABET
                                                if valid_word(letter+
                                                                tiles_to_str(self.board.find_string(coords, 0, 1)))}
                if coords[1]+1 < COLS:
                    CROSS_CHECKS_DOWN[
                        coords[0]][coords[1]+1] = {letter for letter in ALPHABET
                                                if valid_word(tiles_to_str(self.board.find_string(coords, 0, -1))[::-1]+
                                                                letter)}

        for word in words:
            if word[1].coords[0] - word[0].coords[0] == 0:
                across = True
                row = word[1].coords[0]
            else:
                across = False
                col = word[1].coords[1]

            if across:
                if word[0].coords[1]-1 > -1:
                    CROSS_CHECKS_ACROSS[row][word[0].coords[1]-1] = []
                if word[-1].coords[1]+1 < COLS:
                    CROSS_CHECKS_ACROSS[row][word[-1].coords[1]+1] = []
            else:
                if word[0].coords[0]-1 > -1:
                    CROSS_CHECKS_DOWN[word[0].coords[0]-1][col] = []
                if word[-1].coords[0]+1 < ROWS:
                    CROSS_CHECKS_DOWN[word[-1].coords[0]+1][col] = []

    def find_all_moves(self):
        possible_moves = []
        for row in self.board.get_board():
            possible_anchors = []

            for tile in row:
                coords = tile.coords
                board = self.board.get_board()
                if (board[coords[0]+1][coords[1]] in EMPTY_TILES or
                    board[coords[0]-1][coords[1]] in EMPTY_TILES or
                    board[coords[0]][coords[1]+1] in EMPTY_TILES or
                    board[coords[0]][coords[1]-1] in EMPTY_TILES):
                    possible_anchors.append(tile)

            for i, anchor in enumerate(possible_anchors):
                if i > 0:
                    limit = anchor.coords[0] - possible_anchors[i-1].coords[0]
                else:
                    limit = anchor.coords[0]

                partial_word = self.left_part([], limit)

                

    def left_part(self, partial_word: str, square: Tile, limit: int, legal_moves: list[str]):
        legal_moves += self.extend_right(partial_word, square, limit, legal_moves)
        if limit > 0:
            for l in DICTIONARY.itervalues(partial_word):
                if l in self.rack.get_rack_letters:
                    tile = Tile(l)
                    self.rack.remove_tile(tile)
                    self.left_part(partial_word + l, limit - 1, legal_moves)
                    self.rack.add_tile(tile)
        else:
            return partial_word
        
    def extend_right(self, partial_word: str, square: Tile, legal_moves: list[str]):
        next_square = self.next_square(square)
        if square in EMPTY_TILES:
            if tiles_to_str(partial_word) in DICTIONARY.keys():
                legal_moves.append(partial_word)
            for l in DICTIONARY.itervalues(partial_word):
                if (l in self.rack.get_rack_letters() and 
                    l in CROSS_CHECKS_ACROSS[square.coords[0]][square.coords[1]]):
                    tile = Tile(l)
                    self.rack.remove_tile(tile)
                    if square.coords[1] < COLS:
                        legal_moves.append(
                            self.extend_right(partial_word + l, 
                                              next_square, legal_moves))
                    self.rack.add_tile(tile)
        else:
            l = square.letter
            if l in DICTIONARY.itervalues(partial_word):
                legal_moves.append(
                    self.extend_right(partial_word + l, next_square, legal_moves))

        return legal_moves
    
    def next_square(self, square: Tile):
        if square.coords[1]+1 < COLS:
            return self.board.get_board()[square.coords[0]][square.coords[1]+1]
        return None