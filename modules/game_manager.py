from .board import Board
from .drawbag import Drawbag
from .player import Player
import random

class GameManager:
    def __init__(self, player_list: list, board: Board, drawbag: Drawbag):
        self.player_list = player_list
        self.board = board
        self.drawbag = drawbag
        self.turn = None

        self.initialize_game()
        
    def initialize_game(self):
        self.turn = random.randint(0, len(self.player_list) - 1)
        
    def next_turn(self):
        self.turn += 1
        if self.turn >= len(self.player_list):
            self.turn = 0
            
    def play(self, turn: int, move: dict): #TODO
        pass
        
    def get_current_turn(self):
        return self.turn
        
    def get_current_turn_player(self):
        return self.player_list[self.turn]