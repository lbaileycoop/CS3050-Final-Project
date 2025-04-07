"""Module containing the definition for a Rack object"""

from .drawbag import Drawbag
from .tile import Tile

RACK_SIZE = 7


class Rack:
    """
    Class representing the rack of a player

    Attributes:
        rack (List(Tile)): A list containing the tiles a player currenlty has
    """

    def __init__(self, drawbag: Drawbag):
        """Initializes a rack object for the start of the game"""
        self.rack: list[Tile] = []
        self.add_tile(Tile("", 0, "./assets/images/clear.png"))
        self.fill_rack(drawbag)

    def add_tile(self, tile: Tile):
        """Fucntion to add a tile to the current rack"""
        self.rack.append(tile)

    def insert_tile(self, tile: Tile, index: int):
        """Function to insert a tile into a specific position"""
        self.rack.insert(index, tile)

    def get_rack(self) -> list[Tile]:
        """Getter function for the rack list"""
        return self.rack

    def set_rack(self, new_rack: list[Tile]):
        """Setter function for the rack"""
        self.rack = new_rack

    def remove_tile(self, tile: Tile):
        """Removes a specified tile from the rack"""
        self.rack.remove(tile)

    def fill_rack(self, drawbag: Drawbag):
        """Fills all empty spaces in the rack"""
        while len(self.rack) < RACK_SIZE and not drawbag.is_empty():
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
