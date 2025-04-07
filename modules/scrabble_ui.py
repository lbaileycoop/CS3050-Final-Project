"""Module containing the definition for a ScrabbleUI object"""

import random

from .config import (
    arcade,
    ROWS,
    COLS,
    TILE_SIZE,
    TILE_GAP,
    BORDER_X,
    BORDER_Y,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    BOARD_SIZE,
)
from .tile import Tile
from .drawbag import Drawbag
from .player import Player
from .board import Board, ORIGINAL_BOARD
from .utils import to_coords, get_possible_words
from .game_manager import GameManager


class ScrabbleUI(arcade.View):
    """
    Class representing the Scrabble UI
    """

    def __init__(self):
        super().__init__()

        # TODO: should implement a difficulty select on start screen
        self.DIFFICULTY = "hard"

        # TODO: optional but can implement a background select on start screen
        self.BACKGROUND = "gray"
        self.backgrounds = {
            "gray": "./assets/images/gray.jpg",
            "starry": "./assets/images/starry.jpeg",
            "mountains": "./assets/images/mountains.jpeg",
        }

        # Position constants for dynamic graphics
        self.BOARD_START_X = BORDER_X
        self.BOARD_START_Y = BORDER_Y * 1.5
        self.BOARD_SIZE = WINDOW_WIDTH - BORDER_X * 2
        self.RACK_TILE_SPACING = BOARD_SIZE // 6
        self.BUTTON_X = WINDOW_WIDTH - BORDER_X * 0.6
        self.BOARD_CENTER_X = 7 * (TILE_SIZE + TILE_GAP) + BORDER_X
        self.BOARD_CENTER_Y = (ROWS - 8) * (TILE_SIZE + TILE_GAP) + BORDER_Y * 1.5

        # for determining the current held tile
        self.held_tile = None
        self.held_tile_index = None

        # for keeping track of player's rack
        self.rack_tiles = []
        self.original_rack_positions = []

        # initializing game objects
        self.drawbag = Drawbag()
        self.player = Player("You", self.drawbag)
        self.computer = Player("Computer", self.drawbag)
        self.board = Board()

        # initialize game manager
        self.game_manager = GameManager(
            [self.player, self.computer], self.board, self.drawbag
        )

        """ Sprites creation for graphics """
        # displays the current board state
        self.board_sprites: arcade.SpriteList = arcade.SpriteList()
        self.update_board_display()

        # displays player's rack
        self.rack_sprites: arcade.SpriteList = arcade.SpriteList()
        self.rack_graphic = arcade.Sprite("./assets/images/rack.png")
        self.rack_graphic.center_x = int(WINDOW_WIDTH / 2)
        self.rack_graphic.center_y = BORDER_Y * 0.8
        self.rack_sprites.append(self.rack_graphic)
        self.update_rack_display()

        # displays buttons
        self.button_sprites: arcade.SpriteList = arcade.SpriteList()

        self.reset_button = arcade.Sprite("./assets/images/reset_button.png")
        self.reset_button.center_x = self.BUTTON_X
        self.reset_button.center_y = BORDER_Y * 0.8

        self.trade_in_button = arcade.Sprite("./assets/images/trade_in_button.png")
        self.trade_in_button.center_x = self.BUTTON_X
        self.trade_in_button.center_y = BORDER_Y * 0.5

        self.play_word_button = arcade.Sprite("./assets/images/play_word_button.png")
        self.play_word_button.center_x = self.BUTTON_X
        self.play_word_button.center_y = BORDER_Y * 1.1

        self.button_sprites.append(self.trade_in_button)
        self.button_sprites.append(self.reset_button)
        self.button_sprites.append(self.play_word_button)

        # displays miscellaneous graphics
        self.other_sprites: arcade.SpriteList = arcade.SpriteList()

        self.window_background = arcade.Sprite(self.backgrounds[self.BACKGROUND])
        self.window_background.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.window_background.center_x = WINDOW_WIDTH // 2
        self.window_background.center_y = WINDOW_HEIGHT // 2

        self.board_background = arcade.Sprite("./assets/images/background.png")
        self.board_background.size = (BOARD_SIZE * 1.15, BOARD_SIZE * 1.15)
        self.board_background.center_x = self.BOARD_CENTER_X - 7
        self.board_background.center_y = self.BOARD_CENTER_Y

        self.turn_display = arcade.Sprite("./assets/images/turn_display.png")
        self.turn_display.center_x = WINDOW_WIDTH * 0.13
        self.turn_display.center_y = WINDOW_HEIGHT + 30

        self.scoreboard_background = arcade.Sprite(
            "./assets/images/scoreboard_background.png"
        )
        self.scoreboard_background.center_x = WINDOW_WIDTH * 0.13
        self.scoreboard_background.center_y = WINDOW_HEIGHT * 0.58

        self.letter_dist_background = arcade.Sprite(
            "./assets/images/scoreboard_background.png"
        )
        self.letter_dist_background.center_x = WINDOW_WIDTH * 0.87
        self.letter_dist_background.center_y = WINDOW_HEIGHT * 0.58

        self.other_sprites.append(self.window_background)
        self.other_sprites.append(self.board_background)
        self.other_sprites.append(self.turn_display)
        self.other_sprites.append(self.scoreboard_background)
        self.other_sprites.append(self.letter_dist_background)

        # For displaying the game history
        self.game_history = {self.player: [], self.computer: []}

        # Displays all text
        arcade.load_font("./assets/Minecraft.ttf")
        self.update_text_display()

        # If the computer is selected to go first, they move
        if self.game_manager.get_current_turn_player() == self.computer:
            arcade.schedule_once(
                lambda dt: self.computer_turn(
                    self.computer, self.DIFFICULTY, self.drawbag, self.game_manager
                ),
                5,
            )

        # make a save state for the board and player's rack for resetting the turn
        self.save_game_state()

    def computer_turn(self, computer_player_object, difficulty, drawbag, game_manager):
        letters = ""
        num_free_letters = 0
        for tile in computer_player_object.get_rack():
            if tile.letter == "":
                num_free_letters += 1
            else:
                letters += tile.letter

        possible_words = get_possible_words(letters, num_free_letters)
        # TODO: For now just determining word quality by length, but should be changed to score
        sorted_possible_words = sorted(possible_words, key=len)

        word_to_play = ""
        if difficulty == "easy":
            word_to_play = sorted_possible_words[0]
        elif difficulty == "medium":
            word_to_play = sorted_possible_words[len(sorted_possible_words) // 2]
        elif difficulty == "hard":
            word_to_play = sorted_possible_words[len(sorted_possible_words) - 1]
        else:
            word_to_play = sorted_possible_words[
                random.randint(0, len(sorted_possible_words) - 1)
            ]

        print(word_to_play)

        # get corresponding tiles
        tiles_to_play = []
        for ch in word_to_play:
            for i, tile in enumerate(computer_player_object.get_rack()):
                if tile.letter == ch:
                    tiles_to_play.append(computer_player_object.get_rack().pop(i))
                    break

        # TODO: implement actual logic for places the computer should play,
        # for now, just places them where there is empty space
        for row in range(15):
            for col in range(15):
                if (
                    tiles_to_play
                    and self.board.get_board()[row][col].letter
                    == ORIGINAL_BOARD[row][col].letter
                ):
                    tile_to_play = tiles_to_play.pop(0)
                    self.board.update_tile(row, col, tile_to_play)

        # play the turn
        word, is_valid, score = self.board.validate_turn()

        if is_valid:
            computer_player_object.add_score(score)

            # Refill computer rack
            computer_player_object.refill_rack(drawbag)

            game_manager.next_turn()

            self.game_history[computer_player_object].append((word, score))
            self.update_text_display()
            self.update_board_display()

            self.save_game_state()
        else:
            self.reset_turn()
            print("ERROR in computer turn")

    def get_board_position(self, row, col):
        """Calculate the screen position for a board tile at the given row and column."""
        x = col * (TILE_SIZE + TILE_GAP) + self.BOARD_START_X
        y = (ROWS - 1 - row) * (TILE_SIZE + TILE_GAP) + self.BOARD_START_Y
        return x, y

    def get_rack_position(self, tile_index):
        """Calculate the screen position for a rack tile at the given index."""
        x = self.BOARD_START_X + (self.RACK_TILE_SPACING * tile_index)
        y = self.rack_graphic.center_y
        return x, y

    def update_board_display(self):
        """Update the visual representation of the board to match the current board state"""
        # Clear existing board sprites
        self.board_sprites.clear()

        # Create new sprites for each tile on the board
        current_board = self.board.get_board()
        for row in range(ROWS):
            for col in range(COLS):
                _tile = current_board[row][col]
                tile = Tile(_tile.letter, _tile.value, _tile.image_path)

                x, y = self.get_board_position(row, col)
                tile.sprite.center_x = x - 7
                tile.sprite.center_y = y

                self.board_sprites.append(tile.sprite)

    def update_rack_display(self):
        """Update the visual representation of the rack to match the player's rack"""
        # Clear existing rack tiles and positions (except rack graphic)
        for tile in self.rack_tiles:
            if tile.sprite in self.rack_sprites:
                self.rack_sprites.remove(tile.sprite)

        self.rack_tiles = []
        self.original_rack_positions = []

        for i in range(self.player.rack.len_rack()):
            _tile = self.player.get_rack()[i]
            tile = Tile(_tile.letter, _tile.value, _tile.image_path, scale=1.2)

            x, y = self.get_rack_position(i)
            tile.sprite.center_x = x
            tile.sprite.center_y = y

            self.rack_sprites.append(tile.sprite)
            self.rack_tiles.append(tile)
            self.original_rack_positions.append((x, y))

    def update_text_display(self):
        self.text_objects = []

        offset = 20 * len(self.game_history[self.player])

        turn_text = ""
        if self.game_manager.get_current_turn_player().get_name() == "You":
            turn_text = "Your turn!"
        else:
            turn_text = "Computer thinking..."

        self.text_objects = [
            arcade.Text(
                turn_text,
                self.turn_display.center_x - 190,
                self.turn_display.center_y - 75,
                arcade.color.WHITE,
                22,
                380,
                "center",
                "Minecraft",
            ),
            arcade.Text(
                "Scoreboard",
                self.scoreboard_background.center_x - 70,
                self.scoreboard_background.center_y + 240,
                arcade.color.WHITE,
                18,
                font_name="Minecraft",
            ),
            arcade.Text(
                f"Player: {self.player.get_score()}",
                self.scoreboard_background.center_x - 140,
                self.scoreboard_background.center_y + 200,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                f"Computer: {self.computer.get_score()}",
                self.scoreboard_background.center_x - 140,
                (self.scoreboard_background.center_y + 160) - offset,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                "Play Word",
                self.BUTTON_X - 42,
                self.play_word_button.center_y - 6,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                "Reset",
                self.BUTTON_X - 25,
                self.reset_button.center_y - 6,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                "Trade In",
                self.BUTTON_X - 42,
                self.trade_in_button.center_y - 6,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                "Letter Distribution",
                self.letter_dist_background.center_x - 100,
                self.letter_dist_background.center_y + 240,
                arcade.color.WHITE,
                18,
                font_name="Minecraft",
            ),
            arcade.Text(
                "A - 9         N - 6",
                self.letter_dist_background.center_x - 80,
                self.letter_dist_background.center_y + 200,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                "B - 2         O - 8",
                self.letter_dist_background.center_x - 80,
                self.letter_dist_background.center_y + 165,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                "C - 2         P - 2",
                self.letter_dist_background.center_x - 80,
                self.letter_dist_background.center_y + 130,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                "D - 4         Q - 1",
                self.letter_dist_background.center_x - 80,
                self.letter_dist_background.center_y + 95,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                "E - 12        R - 6",
                self.letter_dist_background.center_x - 80,
                self.letter_dist_background.center_y + 60,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                "F - 2          S - 4",
                self.letter_dist_background.center_x - 80,
                self.letter_dist_background.center_y + 25,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                "G - 3          T - 6",
                self.letter_dist_background.center_x - 80,
                self.letter_dist_background.center_y - 10,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                "H - 2          U - 4",
                self.letter_dist_background.center_x - 80,
                self.letter_dist_background.center_y - 45,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                "I - 9           V - 2",
                self.letter_dist_background.center_x - 80,
                self.letter_dist_background.center_y - 80,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                "J - 1           W - 2",
                self.letter_dist_background.center_x - 80,
                self.letter_dist_background.center_y - 115,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                "K - 1           X - 1",
                self.letter_dist_background.center_x - 80,
                self.letter_dist_background.center_y - 150,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                "L - 4          Y - 2",
                self.letter_dist_background.center_x - 80,
                self.letter_dist_background.center_y - 185,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                "M - 2          Z - 1",
                self.letter_dist_background.center_x - 80,
                self.letter_dist_background.center_y - 220,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
        ]

        # For displaying previous turn results
        for i in range(len(self.game_history[self.player])):
            turn = self.game_history[self.player][i]
            word, score = turn[0], turn[1]
            self.text_objects.append(
                arcade.Text(
                    f"+{score}        {word}",
                    self.scoreboard_background.center_x - 100,
                    (self.scoreboard_background.center_y + 180) - 20 * i,
                    arcade.color.WHITE,
                    12,
                    font_name="Minecraft",
                )
            )

        for i in range(len(self.game_history[self.computer])):
            turn = self.game_history[self.computer][i]
            word, score = turn[0], turn[1]
            self.text_objects.append(
                arcade.Text(
                    f"+{score}        {word}",
                    self.scoreboard_background.center_x - 100,
                    (self.scoreboard_background.center_y + 140) - offset - 20 * i,
                    arcade.color.WHITE,
                    12,
                    font_name="Minecraft",
                )
            )

    def swap_rack_tiles(self, index1, index2):
        """Swap two tiles in the player's rack and update the display"""
        # Swap tiles in the player's rack
        rack = self.player.get_rack()
        rack[index1], rack[index2] = rack[index2], rack[index1]

        # Update visuals
        self.update_rack_display()

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that

    def save_game_state(self):
        curr_board = self.board.get_board()
        self.saved_board_state = [[None for _ in range(15)] for _ in range(15)]
        for row in range(15):
            for col in range(15):
                tile = curr_board[row][col]
                self.saved_board_state[row][col] = Tile(
                    tile.letter, tile.value, tile.image_path
                )

        curr_rack = self.player.get_rack()
        self.saved_rack_state = []
        for tile in curr_rack:
            self.saved_rack_state.append(Tile(tile.letter, tile.value, tile.image_path))

    def reset_turn(self):
        """Reset the current turn"""
        # self.board.set_board(self.saved_board_state)
        # self.player.set_rack(self.saved_rack_state)
        self.player.add_tiles(self.board.get_current_turn_tiles())
        self.board.clear_current_turn_tiles()
        self.update_board_display()
        self.update_rack_display()

        # Clear any held tile
        self.held_tile = None
        self.held_tile_index = None

        self.save_game_state()

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # Call draw() on all sprite lists below
        self.other_sprites.draw()
        self.board_sprites.draw()
        self.button_sprites.draw()

        for text_object in self.text_objects:
            text_object.draw()

        self.rack_sprites.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """

        # Make tiles move up slightly to indicate the player hovering over them
        for idx in range(1, len(self.rack_sprites)):
            if self.rack_sprites[idx].collides_with_point((x, y)):
                new_y = self.get_rack_position(idx)[1] + 20
                self.rack_sprites[idx].center_y = new_y
            else:
                _, original_y = self.get_rack_position(idx)
                self.rack_sprites[idx].center_y = original_y

        # Change button colors to indicate player hovering over them
        for button in self.button_sprites:
            if button == self.reset_button:
                image_name = "reset_button"
            elif button == self.trade_in_button:
                image_name = "trade_in_button"
            elif button == self.play_word_button:
                image_name = "play_word_button"
            else:
                continue

            if button.collides_with_point((x, y)):
                button.texture = arcade.load_texture(
                    f"./assets/images/{image_name}_hover.png"
                )
            else:
                button.texture = arcade.load_texture(
                    f"./assets/images/{image_name}.png"
                )

        if self.held_tile:
            self.held_tile.sprite.center_x = x
            self.held_tile.sprite.center_y = y
            # Adjust scale based on whether tile is over the board
            if self.board_background.collides_with_point((x, y)):
                self.held_tile.sprite.scale = 0.63
            else:
                self.held_tile.sprite.scale = 1.2

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        # Check if a rack tile was clicked
        for i, tile in enumerate(self.rack_tiles):
            if tile.sprite.collides_with_point((x, y)):
                self.held_tile = tile
                self.held_tile_index = i
                break

        # Check if a button was clicked
        for button_sprite in self.button_sprites:
            if button_sprite.collides_with_point((x, y)):
                if button_sprite == self.reset_button:
                    self.reset_turn()
                elif button_sprite == self.trade_in_button:
                    # TODO: implement tile trade in
                    pass
                elif button_sprite == self.play_word_button:
                    is_valid, words = self.board.play_turn()
                    if is_valid:
                        score = sum(words.values())

                        curr_player = self.game_manager.get_current_turn_player()
                        curr_player.add_score(score)

                        curr_player.refill_rack(self.drawbag)
                        self.update_rack_display()

                        self.game_manager.next_turn()

                        for word, points in words.items():
                            self.game_history[curr_player].append((word, points))
                        self.update_text_display()

                        arcade.schedule_once(
                            lambda dt: self.computer_turn(
                                self.computer,
                                self.DIFFICULTY,
                                self.drawbag,
                                self.game_manager,
                            ),
                            5,
                        )
                        self.save_game_state()
                    else:
                        self.reset_turn()

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when a user releases a mouse button.
        """
        if self.held_tile:
            placed = False

            # If a tile is dropped over a space on the board, update the board position to that tile
            for i, board_sprite in enumerate(self.board_sprites):
                if board_sprite.collides_with_point((x, y)):
                    col, row = to_coords(i)

                    # ensure tiles can only be played on empty board tiles
                    if (
                        self.board.get_board()[row][col].letter
                        != ORIGINAL_BOARD[row][col].letter
                    ) or self.game_manager.get_current_turn_player() == self.computer:
                        continue

                    letter = self.held_tile.letter
                    value = self.held_tile.value
                    image_path = self.held_tile.image_path

                    new_tile = Tile(letter, value, image_path)
                    self.board.update_tile(row, col, new_tile)

                    board_sprite.texture = arcade.load_texture(image_path)

                    # Remove the tile from player's rack
                    self.player.rack.remove_tile(
                        self.player.get_rack()[self.held_tile_index]
                    )

                    # Update the rack display
                    self.update_rack_display()

                    placed = True
                    break

            # Allow for dragging tiles onto one another in the rack to swap their positions
            if not placed:
                for i, rack_tile in enumerate(self.rack_tiles):
                    if (
                        rack_tile != self.held_tile
                        and rack_tile.sprite.collides_with_point((x, y))
                    ):
                        self.swap_rack_tiles(self.held_tile_index, i)
                        placed = True
                        break

            # If the tile is not dragged to a valid spot on the board, reset it back to rack
            if (
                not placed
                and self.held_tile_index is not None
                and self.held_tile_index < len(self.original_rack_positions)
            ):
                original_x, original_y = self.original_rack_positions[
                    self.held_tile_index
                ]
                self.held_tile.sprite.center_x = original_x
                self.held_tile.sprite.center_y = original_y
                self.held_tile.sprite.scale = 1.2

            self.held_tile = None
            self.held_tile_index = None
