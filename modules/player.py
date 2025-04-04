"""Module containing the definition for a Player object"""

from .drawbag import Drawbag
from .rack import Rack


class Player:
    """
    Class representing a player

    Attributes:
        name (str): The player's name
        rack (Rack): The player's rack of tiles
        score (int): The player's current score
    """

    def __init__(self, name: str, drawbag: Drawbag):
        self.name = name
        self.rack = Rack(drawbag)
        self.score = 0

    def get_name(self):
        """Getter function for the player's name"""
        return self.name

    def get_rack(self):
        """Getter function for the player's current rack"""
        return self.rack.get_rack()

    def set_rack(self, new_rack):
        """Setter function for the player's rack"""
        self.rack.set_rack(new_rack)

    def refill_rack(self, drawbag):
        """Function to refill the player's rack when a turn is played"""
        if drawbag.get_remaining_tiles() and len(self.rack.get_rack()) < 7:
            num_tiles_to_draw = 7 - len(self.rack.get_rack())
            for _ in range(num_tiles_to_draw):
                if drawbag.get_remaining_tiles():
                    self.rack.add_tile(drawbag.draw_tile())

    def get_score(self):
        """Getter function for the player's current sore"""
        return self.score

    def add_score(self, score: int):
        """Function to increment the player's score"""
        self.score += score
