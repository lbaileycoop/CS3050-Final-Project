"""Module containing the definition for a Rack object"""

from .drawbag import Drawbag
from .tile import Tile


class Rack:
    """
    Class representing the rack of a player

    Attributes:
        rack (List(Tile)): A list containing the tiles a player currenlty has
    """

    def __init__(self, drawbag: Drawbag):
        """Initializes a rack object for the start of the game"""
        self.rack: list[Tile] = []
        self.initialize_rack(drawbag)

    def add_tile(self, tile: Tile):
        """Fucntion to add a tile to the current rack"""
        self.rack.append(tile)

    def insert_tile(self, tile: Tile, index: int):
        """Function to insert a tile into a specific position"""
        self.rack.insert(index, tile)

    def get_rack(self):
        """Getter function for the rack list"""
        return self.rack

    def set_rack(self, new_rack):
        """Setter function for the rack"""
        self.rack = new_rack

    def remove_tile(self, tile: Tile):
        """Removes a specified tile from the rack"""
        self.rack.remove(tile)

    def initialize_rack(self, drawbag: Drawbag):
        """Initializes a rack for the beginning of the game with 7 tiles from the draw bag"""
        for _ in range(7):
            self.rack.append(drawbag.draw_tile())

    def len_rack(self):
        """Function to get the amount of tiles in the current rack"""
        return len(self.rack)

    def get_rack_letters(self):
        """Returns a list of letters in the rack"""
        letters: list[str] = []

        for tile in self.rack:
            letters.append(tile.letter)

        return letters

    def remove_letter(self, letter: str):
        """Removes a tile from the rack by letter"""
        for tile in self.rack:
            if tile.letter == letter:
                self.remove_tile(tile)
                break
