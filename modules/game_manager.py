"""Module containing the definition for a GameManager object"""

import random
from .board import Board
from .drawbag import Drawbag
from .player import Player
from .ai import AI


class GameManager:
    """
    Class which contains several methods for controlling scrabble game flow

    Attributes:
        player_list (list(Player)): The game's list of players
        board (Board): The game's board state
        drawbag (Drawbag): The game's drawbag
        turn (int): The current turn, as an index of player_list
    """

    def __init__(self, players: list[tuple[str, str] | tuple[str, str, int]]):
        """Creates a GameManager object"""
        self.board: Board = Board()
        self.drawbag: Drawbag = Drawbag()
        self.turn: int = -1

        self.player_list: list[Player] = []

        for player in players:
            if player[0] == "ai":
                self.player_list.append(AI(player[1], self.drawbag, self.board, 0))
            elif player[0] == "human":
                self.player_list.append(Player(player[1], self.drawbag))
            else:
                print('invalid player type! should be "human" or "ai"')

        self.initialize_game()

    def initialize_game(self):
        """Starts the scrabble game by choosing a random player to act first"""
        self.turn = random.randint(0, len(self.player_list) - 1)

    def next_turn(self):
        """Switches the turn to the next player in rotation"""
        self.turn = (self.turn + 1) % len(self.player_list)

    def get_current_turn(self) -> int:
        """Getter function for the current turn as an integer"""
        return self.turn

    def get_current_turn_player(self) -> Player:
        """Getter function for the current turn as a Player"""
        return self.player_list[self.turn]

    def get_drawbag(self) -> Drawbag:
        """Getter function for the drawbag"""
        return self.drawbag

    def get_board(self) -> Board:
        """Getter function for the board"""
        return self.board

    def get_player_list(self) -> list[Player]:
        """Getter function for the list of players"""
        return self.player_list

    def end_game(self):
        """Ends the game and returns the winner"""
        scores = {}

        unplayed_value = 0
        emptied_players: list[str] = []

        for player in self.player_list:
            score = player.get_score()
            for tile in player.get_rack_tiles():
                score -= tile.get_value()
                unplayed_value += tile.get_value()
            if player.rack_is_empty():
                emptied_players.append(player.get_name())
            scores[player.get_name()] = score

        for player in emptied_players:
            scores[player] += unplayed_value
        scores = {player.get_name(): player.get_score() for player in self.player_list}

        return scores
