from .tile import Tile, TILES

class Board():
    """
    Class representing the Scrabble board

    Attributes:
        board (lst) : 2D list representing the board's current state
    """
    def __init__(self):
        """ Initialize a board object """

        # 2D list to store the current board state
        self.board = [
            [TILES["triple_word"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_word"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["triple_word"]],
            [TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"]],
            [TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"]],
            [TILES["double_letter"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["double_letter"]],
            [TILES["base"], TILES["base"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["base"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["base"], TILES["base"]],
            [TILES["base"], TILES["triple_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_letter"], TILES["base"]],
            [TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"]],
            [TILES["triple_word"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["star"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["triple_word"]],
            [TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"]],
            [TILES["base"], TILES["triple_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_letter"], TILES["base"]],
            [TILES["base"], TILES["base"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["base"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["base"], TILES["base"]],
            [TILES["double_letter"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["double_letter"]],
            [TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"]],
            [TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"]],
            [TILES["triple_word"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_word"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["triple_word"]],
        ]
    
    def get_board(self):
        """ Getter function for the current board """
        return self.board

    def update_tile(self, x: int, y: int, tile: Tile):
        """ Function to update a tile in the board """
        self.board[y][x] = tile