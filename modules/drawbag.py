""" Module containing the definition for a Drawbag object """

from random import shuffle
from .tile import Tile, TILES

class Drawbag():
    """
    Class representing the draw bag

    Attributes:
        drawbag (lst): A list containing the tiles in the draw bag
    """
    def __init__(self):
        """ Initializes a draw bag object """
        self.drawbag = []
        self.initialize_drawbag()

    def add_tile(self, tile: Tile, quantity: int):
        """ Function to add a tile to the draw bag """
        for _ in range(quantity):
            self.drawbag.append(tile)

    def initialize_drawbag(self):
        """ Function to initialize the draw bag with the proper letter distribution """
        self.add_tile(TILES["a"], 9)
        self.add_tile(TILES["b"], 2)
        self.add_tile(TILES["c"], 2)
        self.add_tile(TILES["d"], 4)
        self.add_tile(TILES["e"], 12)
        self.add_tile(TILES["f"], 2)
        self.add_tile(TILES["g"], 3)
        self.add_tile(TILES["h"], 2)
        self.add_tile(TILES["i"], 9)
        self.add_tile(TILES["j"], 1)
        self.add_tile(TILES["k"], 1)
        self.add_tile(TILES["l"], 4)
        self.add_tile(TILES["m"], 2)
        self.add_tile(TILES["n"], 6)
        self.add_tile(TILES["o"], 8)
        self.add_tile(TILES["p"], 2)
        self.add_tile(TILES["q"], 1)
        self.add_tile(TILES["r"], 6)
        self.add_tile(TILES["s"], 4)
        self.add_tile(TILES["t"], 6)
        self.add_tile(TILES["u"], 4)
        self.add_tile(TILES["v"], 2)
        self.add_tile(TILES["w"], 2)
        self.add_tile(TILES["x"], 1)
        self.add_tile(TILES["y"], 2)
        self.add_tile(TILES["z"], 1)
        self.add_tile(TILES["blank"], 2)
        shuffle(self.drawbag)

    def draw_tile(self):
        """ Function to simulate drawing a tile from the draw bag """
        return self.drawbag.pop()

    def get_remaining_tiles(self):
        """ Function to get the amount of tiles remaining in the draw bag """
        return len(self.drawbag)
