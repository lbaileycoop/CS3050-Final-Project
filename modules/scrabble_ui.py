"""Module containing the definition for a ScrabbleUI object"""

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
from .board import Board, ORIGINAL_BOARD, EMPTY_TILES
from .utils import from_coords, to_coords, get_possible_words
from .game_manager import GameManager

import random


class ScrabbleUI(arcade.View):
    """
    Class representing the Scrabble UI
    """

    def __init__(self):
        super().__init__()

        # TODO: should implement a difficulty select on start screen
        self.difficulty = "hard"

        # TODO: optional but can implement a background select on start screen
        self.background = "gray"
        self.backgrounds = {
            "gray": "./assets/images/gray.jpg",
            "starry": "./assets/images/starry.jpeg",
            "mountains": "./assets/images/mountains.jpeg",
        }

        # Position constants for dynamic graphics
        self.board_start_x = BORDER_X
        self.board_start_y = BORDER_Y * 1.5
        self.board_size = WINDOW_WIDTH - BORDER_X * 2
        self.rack_tile_spacing = BOARD_SIZE // 6
        self.button_x = WINDOW_WIDTH - BORDER_X * 0.6
        self.board_center_x = 7 * (TILE_SIZE + TILE_GAP) + BORDER_X
        self.board_center_y = (ROWS - 8) * (TILE_SIZE + TILE_GAP) + BORDER_Y * 1.5

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

        self.reset_button = arcade.Sprite("./assets/images/blue_button.png")
        self.reset_button.center_x = self.BUTTON_X
        self.reset_button.center_y = BORDER_Y * 0.8

        self.trade_in_button = arcade.Sprite("./assets/images/green_button.png")
        self.trade_in_button.center_x = self.BUTTON_X
        self.trade_in_button.center_y = BORDER_Y * 0.5

        self.play_word_button = arcade.Sprite("./assets/images/red_button.png")
        self.play_word_button.center_x = self.BUTTON_X
        self.play_word_button.center_y = BORDER_Y * 1.1

        self.button_sprites.append(self.trade_in_button)
        self.button_sprites.append(self.reset_button)
        self.button_sprites.append(self.play_word_button)

        # For displaying pop up messages
        self.popup = arcade.SpriteList()

        self.box = arcade.Sprite("./assets/images/turn_display.png")
        self.box.size = (WINDOW_WIDTH // 3, WINDOW_HEIGHT // 3)
        self.box.center_x = self.BOARD_CENTER_X
        self.box.center_y = self.BOARD_CENTER_Y

        self.popup.append(self.box)

        self.done_button = arcade.SpriteList()
        self._done_button = arcade.Sprite("./assets/images/green_button.png")
        self._done_button.center_x = self.BOARD_CENTER_X
        self._done_button.center_y = self.BOARD_CENTER_Y - 100
        self.done_button.append(self._done_button)

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

        self.bingo = False
        self.trade_in_active = False

        # Displays all text
        arcade.load_font("./assets/Minecraft.ttf")
        self.update_text_display()

        # If the computer is selected to go first, they move
        if self.game_manager.get_current_turn_player() == self.computer:
            arcade.schedule_once(
                lambda dt: # TODO: ADD AI TURN HERE
                ),
                1,
            )

        # make a save state for the board and player's rack for resetting the turn
        self.save_game_state()

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

        self.text_objects = [
            arcade.Text(
                f'{"Your turn!" if self.game_manager.get_current_turn_player().get_name() == "You" else "Computer Thinking..."}',
                self.turn_display.center_x,
                self.turn_display.center_y - 65,
                arcade.color.WHITE,
                22,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ),
            arcade.Text(
                "Scoreboard",
                self.scoreboard_background.center_x,
                self.scoreboard_background.center_y + 250,
                arcade.color.WHITE,
                18,
                align="center",
                anchor_x="center",
                anchor_y="center",
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
                self.BUTTON_X,
                self.play_word_button.center_y,
                arcade.color.WHITE,
                14,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ),
            arcade.Text(
                "Reset",
                self.BUTTON_X,
                self.reset_button.center_y,
                arcade.color.WHITE,
                14,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ),
            arcade.Text(
                "Trade In",
                self.BUTTON_X,
                self.trade_in_button.center_y,
                arcade.color.WHITE,
                14,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ),
            arcade.Text(
                "Letter Distribution",
                self.letter_dist_background.center_x,
                self.letter_dist_background.center_y + 250,
                arcade.color.WHITE,
                18,
                align="center",
                anchor_x="center",
                anchor_y="center",
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
            arcade.Text(
                "Blank - 2",
                self.letter_dist_background.center_x,
                self.letter_dist_background.center_y - 250,
                arcade.color.WHITE,
                14,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ),
        ]

        # For displaying previous turn results
        if len(self.game_history[self.player]) > 10:
            self.game_history.pop(0)
        if len(self.game_history[self.computer]) > 10:
            self.game_history.pop(0)

        for i in range(len(self.game_history[self.player])):
            turn = self.game_history[self.player][i]
            word, score = turn[0], turn[1]
            self.text_objects.append(
                arcade.Text(
                    f"+{score}",
                    self.scoreboard_background.center_x - 100,
                    (self.scoreboard_background.center_y + 180) - 20 * i,
                    arcade.color.WHITE,
                    12,
                    font_name="Minecraft",
                )
            )
            self.text_objects.append(
                arcade.Text(
                    word,
                    self.scoreboard_background.center_x,
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
                    f"+{score}",
                    self.scoreboard_background.center_x - 100,
                    (self.scoreboard_background.center_y + 140) - offset - 20 * i,
                    arcade.color.WHITE,
                    12,
                    font_name="Minecraft",
                )
            )
            self.text_objects.append(
                arcade.Text(
                    word,
                    self.scoreboard_background.center_x,
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
        """Save game state preserving original tile references"""
        self.saved_board_state = []
        for row in range(15):
            board_row = []
            for col in range(15):
                current_tile = self.board.get_board()[row][col]
                original_tile = ORIGINAL_BOARD[row][col]

                # Preserve original tile objects where possible
                if current_tile.letter == original_tile.letter:
                    board_row.append(original_tile)
                else:
                    board_row.append(
                        Tile(
                            current_tile.letter,
                            current_tile.value,
                            current_tile.image_path,
                        )
                    )
            self.saved_board_state.append(board_row)

        self.saved_rack_state = [
            Tile(t.letter, t.value, t.image_path) for t in self.player.get_rack()
        ]
        self.saved_first_turn = self.board.first_turn

    def reset_turn(self):
        """Reset the turn using original tile references"""
        # Restore board with original tile objects
        new_board = []
        for row in range(15):
            board_row = []
            for col in range(15):
                saved_tile = self.saved_board_state[row][col]
                original_tile = ORIGINAL_BOARD[row][col]

                # Use original tile object if it matches
                if saved_tile.letter == original_tile.letter:
                    board_row.append(original_tile)
                else:
                    board_row.append(saved_tile)
            new_board.append(board_row)

        self.board.set_board(new_board)
        self.board.first_turn = self.saved_first_turn
        self.player.set_rack(self.saved_rack_state)

        self.update_board_display()
        self.update_rack_display()
        self.held_tile = None
        self.held_tile_index = None
        self.save_game_state()

    def on_draw(self):
        """
        Render the screen.
        """
        self.clear()

        # Call draw() on all sprite lists below
        self.other_sprites.draw()
        self.board_sprites.draw()
        self.button_sprites.draw()

        for text_object in self.text_objects:
            text_object.draw()

        # Draw blank tile prompt if active
        if hasattr(self, "text_input_active") and self.text_input_active:
            self.popup.draw()
            arcade.Text(
                "Select a letter for the blank tile:",
                self.board_center_x,
                self.board_center_y + 25,
                arcade.color.WHITE,
                16,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ).draw()
            arcade.Text(
                "(Press a letter key or ESC to cancel)",
                self.board_center_x,
                self.board_center_y - 25,
                arcade.color.WHITE,
                16,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ).draw()

        if self.bingo:
            self.popup.draw()
            arcade.Text(
                f"BINGO! +50 points",
                self.board_center_x,
                self.board_center_y + 50,
                arcade.color.WHITE,
                16,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ).draw()
            arcade.Text(
                f"All 7 tiles used!",
                self.board_center_x,
                self.board_center_y,
                arcade.color.WHITE,
                16,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ).draw()
            arcade.Text(
                "Click anywhere on screen to continue",
                self.board_center_x,
                self.board_center_y - 50,
                arcade.color.WHITE,
                16,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ).draw()

        if self.trade_in_active:
            self.popup.draw()
            arcade.Text(
                "Drag tiles here to trade in.",
                self.board_center_x,
                self.board_center_y + 25,
                arcade.color.WHITE,
                16,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ).draw()
            arcade.Text(
                "(Press ESC to cancel)",
                self.board_center_x,
                self.board_center_y - 25,
                arcade.color.WHITE,
                16,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ).draw()
            self.done_button.draw()
            arcade.Text(
                "Done",
                self._done_button.center_x,
                self._done_button.center_y,
                arcade.color.WHITE,
                16,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ).draw()

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
                original_x, original_y = self.get_rack_position(idx)
                self.rack_sprites[idx].center_y = original_y

        # Change button colors to indicate player hovering over them
        for button in self.button_sprites:
            if button == self.reset_button:
                image_name = "blue_button"
            elif button == self.trade_in_button:
                image_name = "green_button"
            elif button == self.play_word_button:
                image_name = "red_button"
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

        if self._done_button.collides_with_point((x, y)):
            self._done_button.texture = arcade.load_texture(
                f"./assets/images/green_button_hover.png"
            )
        else:
            self._done_button.texture = arcade.load_texture(
                f"./assets/images/green_button.png"
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
        if self.bingo:
            self.bingo = False

        # Check if a rack tile was clicked
        for i, tile in enumerate(self.rack_tiles):
            if tile.sprite.collides_with_point((x, y)):
                self.held_tile = tile
                self.held_tile_index = i
                break
        if self._done_button.collides_with_point((x, y)):
            self.game_manager.get_current_turn_player().refill_rack(self.drawbag)
            self.update_rack_display()
            self.trade_in_active = False
            self.game_manager.next_turn()
            self.update_text_display()
            arcade.schedule_once(
                lambda dt: # TODO: ADD AI TURN HERE
                ),
                1,
            )
            self.save_game_state()
        if not self.trade_in_active:
            # Check if a button was clicked
            for button_sprite in self.button_sprites:
                if button_sprite.collides_with_point((x, y)):
                    if button_sprite == self.reset_button:
                        self.reset_turn()
                    elif button_sprite == self.trade_in_button:
                        self.trade_in_active = True
                    elif button_sprite == self.play_word_button:
                        word, is_valid, score = self.board.validate_turn()
                        print(is_valid, score)
                        if is_valid:
                            curr_player = self.game_manager.get_current_turn_player()

                            if len(curr_player.get_rack()) == 0:
                                self.bingo = True
                                score += 50

                                if self.drawbag.is_empty():
                                    self.game_manager.end_game()

                            curr_player.add_score(score)

                            curr_player.refill_rack(self.drawbag)

                            self.update_rack_display()

                            self.game_manager.next_turn()

                            self.game_history[curr_player].append((word, score))
                            self.update_text_display()

                            arcade.schedule_once(
                                lambda dt: # TODO: ADD AI TURN HERE
                                ),
                                1,
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

            # If a tile is dropped over a space on the board
            for i, board_sprite in enumerate(self.board_sprites):
                if (
                    board_sprite.collides_with_point((x, y))
                    and not self.trade_in_active
                ):
                    col, row = to_coords(i)

                    # ensure tiles can only be played on empty board tiles
                    if (
                        self.board.get_board()[row][col].letter
                        != ORIGINAL_BOARD[row][col].letter
                        or self.game_manager.get_current_turn_player() == self.computer
                    ):
                        continue

                    # Handle blank tile placement
                    if self.held_tile.letter == "":  # This is a blank tile
                        # Remove the blank tile from player's rack
                        self.player.rack.remove_tile(
                            self.player.get_rack()[self.held_tile_index]
                        )

                        # Prompt user to select a letter for the blank tile
                        self.blank_tile_prompt = True
                        self.blank_tile_position = (row, col)
                        self.blank_tile_value = 0  # Blank tiles have 0 value

                        # Create a temporary text input
                        self.letter_input = ""
                        self.text_input_active = True

                        # Update display
                        self.update_rack_display()
                        placed = True
                        break
                    else:
                        # Regular tile placement
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

            if not placed and self.trade_in_active:
                if self.box.collides_with_point((x, y)) and self.held_tile:
                    self.drawbag.add_tile(self.player.get_rack()[self.held_tile_index])
                    self.player.rack.remove_tile(
                        self.player.get_rack()[self.held_tile_index]
                    )
                    self.update_rack_display()
                    placed = True

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

    def on_key_press(self, key, modifiers):
        """
        Handle keyboard input for blank tile letter selection
        """
        if hasattr(self, "text_input_active") and self.text_input_active:
            if 97 <= key <= 122:
                letter = chr(key).upper()
                row, col = self.blank_tile_position

                new_tile = Tile(letter, 0, f"./assets/images/{letter}.png")
                self.board.update_tile(row, col, new_tile)

                self.update_board_display()

                self.text_input_active = False
                del self.blank_tile_prompt
                del self.blank_tile_position
                return

            elif key == arcade.key.ESCAPE:
                self.text_input_active = False
                del self.blank_tile_prompt
                del self.blank_tile_position
                return

        if self.trade_in_active:
            if key == arcade.key.ESCAPE:
                self.trade_in_active = False
                self.reset_turn()
                return
