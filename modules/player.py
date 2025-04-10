"""Module containing the definition for a Player object"""

from .drawbag import Drawbag
from .rack import Rack
from .tile import Tile


class Player:
    """
    Class representing a player

    Attributes:
        name (str): The player's name
        rack (Rack): The player's rack of tiles
        score (int): The player's current score
    """

    def __init__(self, name: str, drawbag: Drawbag):
        self.name: str = name
        self.rack: Rack = Rack(drawbag)
        self.score: int = 0

    def get_name(self) -> str:
        """Getter function for the player's name"""
        return self.name

    def get_rack(self) -> Rack:
        """Getter function for the player's current rack"""
        return self.rack

    def get_rack_tiles(self) -> list[Tile]:
        """Getter function for the player's current rack as a list of tiles"""
        return self.rack.get_rack()

    def set_rack(self, new_rack: Rack):
        """Setter function for the player's rack"""
        self.rack.set_rack(new_rack)

    def refill_rack(self, drawbag: Drawbag):
        """Function to refill the player's rack when a turn is played"""
        self.rack.fill_rack(drawbag)

    def get_score(self) -> int:
        """Getter function for the player's current sore"""
        return self.score

    def add_score(self, score: int):
        """Function to increment the player's score"""
        self.score += score

    def add_tiles(self, tiles: list[Tile]):
        """Adds tiles to the rack from a passed list of tiles"""
        for tile in tiles:
            self.rack.add_tile(Tile.copy(tile))
