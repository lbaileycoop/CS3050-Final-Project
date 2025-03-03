from .drawbag import Drawbag
from .rack import Rack

class Player():
    """
    Class representing a player

    Attributes:
        name (str): The player's name
        rack (Rack): The player's rack of tiles
        score (int): The player's current score
    """
    def __init__(self, name: str, drawbag: Drawbag):
        """ Initializes a player object """
        self.name = name
        self.rack = Rack(drawbag)
        self.score = 0

    def get_rack(self):
        """ Getter function for the player's current rack """
        return self.rack.get_rack()
    
    def get_score(self):
        """ Getter function for the player's current sore """
        return self.score
    
    def add_score(self, score: int):
        """ Function to increment the player's score """
        self.score += score