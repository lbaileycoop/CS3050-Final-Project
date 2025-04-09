"""Module containing the definition for a GameManager object"""

import random
from .board import Board
from .drawbag import Drawbag
from .player import Player


class GameManager:
    """
    Class which contains several methods for controlling scrabble game flow

    Attributes:
    player_list (list(Player)): The game's list of players
    board (Board): The game's board state
    drawbag (Drawbag): The game's drawbag
    turn (int): The current turn, as an index of player_list
    """

    def __init__(self, player_list: list[Player], board: Board, drawbag: Drawbag):
        """Creates a GameManager object"""
        self.player_list: list[Player] = player_list
        self.board: Board = board
        self.drawbag: Drawbag = drawbag
        self.turn: int = -1

        self.initialize_game()

    def initialize_game(self):
        """Starts the scrabble game by choosing a random player to act first"""
        self.turn = random.randint(0, len(self.player_list) - 1)

    def next_turn(self) -> Player:
        """Switches the turn to the next player in rotation and returns the new player"""
        self.turn = (self.turn + 1) % len(self.player_list)
        return self.get_current_turn_player()

    def get_current_turn(self) -> int:
        """Getter function for the current turn as an integer"""
        return self.turn

    def get_current_turn_player(self) -> Player:
        """Getter function for the current turn as a Player"""
        return self.player_list[self.turn]
