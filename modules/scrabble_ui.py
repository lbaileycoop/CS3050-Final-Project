"""Module containing the definition for a ScrabbleUI object"""

import random
from .config import (
    arcade,
    SIZE,
    BORDER_Y,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    BOARD_SIZE,
    BUTTON_X,
    BOARD_CENTER_X,
    BOARD_CENTER_Y,
    BACKGROUND_COORDS,
    LETTER_DIST,
)
from .tile import Tile
from .board import EMPTY_TILES
from .utils import to_coords, get_rack_position, get_board_position
from .game_manager import GameManager
from .player import Player
from .ai import AI


# suppress warning for too many attributes
# pylint: disable=R0902
class ScrabbleUI(arcade.View):
    """
    Class representing the Scrabble UI
    """

    def __init__(self):
        super().__init__()

        # initialize game manager
        self.game_manager = GameManager(
            [
                ("human", "player", 0),
                ("ai", "computer", 2),
            ]
        )

        # For displaying the game history
        self.game_history: dict[Player : list[int]] = {}

        for player in self.game_manager.get_player_list():
            self.game_history[player] = []

        # for determining the current held tile
        self.held_tile: Tile = None
        self.held_tile_index: int = -1

        self.bingo: bool = False

        # Remember # of turns skipped in a row
        self.skip_count: int = 0

        # Get input for traded tiles
        self.trade_in_active: bool = False
        self.tiles_to_trade: list[Tile] = []

        # Get input for blank tiles
        self.text_input_active: bool = False
        self.blank_tile_position: tuple[int, int] = None

        """ Sprites creation for graphics """
        # displays the current board state
        self.board_sprites: arcade.SpriteList = arcade.SpriteList()

        # displays player's rack
        self.rack_sprites: arcade.SpriteList = arcade.SpriteList()

        # displays buttons
        self.button_sprites: arcade.SpriteList = arcade.SpriteList()

        button_names = ["play_word", "reset", "shuffle", "trade_in"]
        for i, name in enumerate(button_names):
            self.button_sprites.append(
                arcade.Sprite(
                    f"./assets/images/{name}_button.png",
                    center_x=BUTTON_X,
                    center_y=BORDER_Y * (1.1 - (i * 0.2)),
                )
            )

        self.background_sprites: arcade.SpriteList = arcade.SpriteList()

        window_background = arcade.Sprite(
            "./assets/images/gray.jpg",
            center_x=WINDOW_WIDTH // 2,
            center_y=WINDOW_HEIGHT // 2,
        )
        window_background.size = (WINDOW_WIDTH, WINDOW_HEIGHT)

        board_background = arcade.Sprite(
            "./assets/images/background.png",
            center_x=BACKGROUND_COORDS["board"][0],
            center_y=BACKGROUND_COORDS["board"][1],
        )
        board_background.size = (BOARD_SIZE * 1.15, BOARD_SIZE * 1.15)

        turn_display = arcade.Sprite(
            "./assets/images/turn_display.png",
            center_x=BACKGROUND_COORDS["turn_display"][0],
            center_y=BACKGROUND_COORDS["turn_display"][1],
        )

        scoreboard_background = arcade.Sprite(
            "./assets/images/scoreboard_background.png",
            center_x=BACKGROUND_COORDS["scoreboard"][0],
            center_y=BACKGROUND_COORDS["scoreboard"][1],
        )

        letter_dist_background = arcade.Sprite(
            "./assets/images/scoreboard_background.png",
            center_x=BACKGROUND_COORDS["letter_dist"][0],
            center_y=BACKGROUND_COORDS["letter_dist"][1],
        )

        rack_background = arcade.Sprite(
            "./assets/images/rack.png",
            center_x=BACKGROUND_COORDS["rack"][0],
            center_y=BACKGROUND_COORDS["rack"][1],
        )

        self.background_sprites.append(window_background)
        self.background_sprites.append(board_background)
        self.background_sprites.append(turn_display)
        self.background_sprites.append(scoreboard_background)
        self.background_sprites.append(letter_dist_background)
        self.background_sprites.append(rack_background)

        # Displays all text
        self.text_objects: list[arcade.Text] = []
        arcade.load_font("./assets/Minecraft.ttf")

        # For displaying pop up messages
        self.popup: arcade.Sprite = arcade.Sprite(
            "./assets/images/turn_display.png",
            center_x=BOARD_CENTER_X,
            center_y=BOARD_CENTER_Y,
        )
        self.popup.size = (WINDOW_WIDTH // 3, WINDOW_HEIGHT // 3)

        self.done_button: arcade.Sprite = arcade.Sprite(
            "./assets/images/trade_in_button.png",
            center_x=BOARD_CENTER_X,
            center_y=BOARD_CENTER_Y - 100,
        )

        self.update_displays()
        self.next_turn()

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """

        # Make tiles move up slightly to indicate the player hovering over them
        if self.background_sprites[5].collides_with_point((x, y)):
            for i, sprite in enumerate(self.rack_sprites):
                if sprite.collides_with_point((x, y)):
                    new_y = get_rack_position(i)[1] + 20
                    sprite.center_y = new_y
                else:
                    _, original_y = get_rack_position(i)
                    sprite.center_y = original_y

        image_names = [
            "play_word_button",
            "reset_button",
            "shuffle_button",
            "trade_in_button",
        ]
        # Change button colors to indicate player hovering over them
        for i, sprite in enumerate(self.button_sprites):
            if sprite.collides_with_point((x, y)):
                sprite.texture = arcade.load_texture(
                    f"./assets/images/{image_names[i]}_hover.png"
                )
            else:
                sprite.texture = arcade.load_texture(
                    f"./assets/images/{image_names[i]}.png"
                )

        if self.done_button.collides_with_point((x, y)):
            self.done_button.texture = arcade.load_texture(
                "./assets/images/trade_in_button_hover.png"
            )
        else:
            self.done_button.texture = arcade.load_texture(
                "./assets/images/trade_in_button.png"
            )

        if self.held_tile:
            self.held_tile.sprite.center_x = x
            self.held_tile.sprite.center_y = y
            # Adjust scale based on whether tile is over the board
            if (
                self.background_sprites[1].collides_with_point((x, y))
                and not self.trade_in_active
            ):
                self.held_tile.sprite.scale = 0.63
            else:
                self.held_tile.sprite.scale = 1.2

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        # Check if a rack tile was clicked
        if not isinstance(self.game_manager.get_current_turn_player(), AI):
            for i, tile in enumerate(
                self.game_manager.get_current_turn_player().get_rack_tiles()
            ):
                if tile.sprite.collides_with_point((x, y)):
                    self.held_tile = tile
                    self.held_tile_index = i
                    break

        if not self.trade_in_active:
            # Check if a button was clicked
            for i, sprite in enumerate(self.button_sprites):
                if sprite.collides_with_point((x, y)):
                    if i == 0:
                        self.play_turn()
                    elif i == 1:
                        self.reset_turn()
                    elif i == 2:
                        self.shuffle_rack()
                    elif i == 3:
                        self.trade_in()
        elif self.done_button.collides_with_point((x, y)):
            self.game_manager.get_current_turn_player().refill_rack(
                self.game_manager.get_drawbag()
            )
            self.game_history[self.game_manager.get_current_turn_player()].append(0)

            if len(self.tiles_to_trade) == 0:
                self.skip_turn()
                return

            self.next_turn()

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when a user releases a mouse button.
        """
        if self.held_tile:
            placed = False

            # If a tile is dropped over a space on the board, update the board position to that tile
            for i, board_sprite in enumerate(self.board_sprites):
                if (
                    board_sprite.collides_with_point((x, y))
                    and not self.trade_in_active
                ):
                    col, row = to_coords(i)

                    # ensure tiles can only be played on empty board tiles
                    if self.game_manager.get_board().get_tile_at(
                        row, col
                    ) not in EMPTY_TILES or isinstance(
                        self.game_manager.get_current_turn_player(), AI
                    ):
                        continue

                    new_tile = Tile.copy(self.held_tile)

                    if new_tile.letter == "":  # This is a blank tile

                        # Prompt user to select a letter for the blank tile
                        self.text_input_active = True
                        self.blank_tile_position = (row, col)

                        # Update display
                        self.update_rack_display()
                    else:
                        self.game_manager.get_board().update_tile(row, col, new_tile)

                    board_sprite.texture = arcade.load_texture(new_tile.image_path)

                    # Remove the tile from player's rack
                    self.game_manager.get_current_turn_player().get_rack().remove_tile(
                        self.game_manager.get_current_turn_player().get_rack_tiles()[
                            self.held_tile_index
                        ]
                    )

                    # Update the rack display
                    self.update_rack_display()

                    placed = True
                    break

            if not placed and self.trade_in_active:
                if self.popup.collides_with_point((x, y)) and self.held_tile:
                    self.game_manager.get_current_turn_player().get_rack().remove_tile(
                        self.held_tile
                    )
                    self.tiles_to_trade.append(self.held_tile)
                    self.update_rack_display()
                    placed = True

            # Allow for dragging tiles onto one another in the rack to swap their positions
            if not placed:
                curr_rack = self.game_manager.get_current_turn_player().get_rack_tiles()
                for i, rack_tile in enumerate(curr_rack):
                    if (
                        rack_tile != self.held_tile
                        and rack_tile.sprite.collides_with_point((x, y))
                    ):
                        curr_rack[self.held_tile_index], curr_rack[i] = (
                            curr_rack[i],
                            curr_rack[self.held_tile_index],
                        )

                        self.update_displays()
                        placed = True
                        break

            # If the tile is not dragged to a valid spot on the board, reset it back to rack
            if not placed and not self.held_tile_index == -1:
                original_x, original_y = get_rack_position(self.held_tile_index)
                self.held_tile.sprite.center_x = original_x
                self.held_tile.sprite.center_y = original_y
                self.held_tile.sprite.scale = 1.2

            self.held_tile = None
            self.held_tile_index = -1

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # Call draw() on all sprite lists below
        self.background_sprites.draw()
        self.board_sprites.draw()
        self.button_sprites.draw()

        for text_object in self.text_objects:
            text_object.draw()

        self.draw_popups()

        self.rack_sprites.draw()

    def draw_popups(self):
        """Draws any popups which are currently active"""
        # Draw blank tile prompt if active
        if self.text_input_active:
            arcade.draw_sprite(self.popup)
            arcade.Text(
                "Select a letter for the blank tile:",
                BOARD_CENTER_X,
                BOARD_CENTER_Y + 25,
                arcade.color.WHITE,
                16,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ).draw()
            arcade.Text(
                "(Press any letter key)",
                BOARD_CENTER_X,
                BOARD_CENTER_Y - 25,
                arcade.color.WHITE,
                16,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ).draw()

        if self.bingo:
            arcade.draw_sprite(self.popup)
            arcade.Text(
                "BINGO! +50 points",
                BOARD_CENTER_X,
                BOARD_CENTER_Y + 50,
                arcade.color.WHITE,
                16,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ).draw()
            arcade.Text(
                "All 7 tiles used!",
                BOARD_CENTER_X,
                BOARD_CENTER_Y,
                arcade.color.WHITE,
                16,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ).draw()
            arcade.Text(
                "Press ESC to close",
                BOARD_CENTER_X,
                BOARD_CENTER_Y - 50,
                arcade.color.WHITE,
                16,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ).draw()

        if self.trade_in_active:
            arcade.draw_sprite(self.popup)
            arcade.Text(
                "Drag tiles here to trade in.",
                BOARD_CENTER_X,
                BOARD_CENTER_Y + 30,
                arcade.color.WHITE,
                16,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ).draw()
            arcade.Text(
                "Tiles chosen: "
                + ", ".join(
                    [
                        ("blank" if tile.letter == "" else tile.letter)
                        for tile in self.tiles_to_trade
                    ]
                ),
                BOARD_CENTER_X,
                BOARD_CENTER_Y,
                arcade.color.WHITE,
                16,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ).draw()
            arcade.Text(
                "(Press ESC to cancel)",
                BOARD_CENTER_X,
                BOARD_CENTER_Y - 30,
                arcade.color.WHITE,
                16,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ).draw()
            arcade.draw_sprite(self.done_button)
            arcade.Text(
                "Done",
                self.done_button.center_x,
                self.done_button.center_y,
                arcade.color.WHITE,
                16,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ).draw()

    def on_key_press(self, symbol, modifiers):
        """
        Handle keyboard input for blank tile letter selection
        """
        if self.text_input_active:
            if 97 <= symbol <= 122:
                letter = chr(symbol).lower()
                row, col = self.blank_tile_position

                new_tile = Tile(letter, 0, f"./assets/images/{letter}.png")
                self.game_manager.get_board().update_tile(row, col, new_tile)

                self.update_board_display()

                self.text_input_active = False
                self.blank_tile_position = None
                return

        if symbol == arcade.key.ESCAPE:
            if self.trade_in_active:
                self.trade_in_active = False
                self.game_manager.get_current_turn_player().add_tiles(
                    self.tiles_to_trade
                )
                self.tiles_to_trade.clear()
                self.reset_turn()
                return
            if self.bingo:
                self.bingo = False

    def play_turn(self):
        """
        Confirms the played turn's legality and performs
        the logic needed to finish a played turn
        """
        is_valid, words, is_bingo = self.game_manager.get_board().play_turn()
        if is_valid:
            score = sum(words.values())

            if is_bingo:
                score += 50
                self.bingo = True

            self.game_manager.get_current_turn_player().add_score(score)

            self.game_history[self.game_manager.get_current_turn_player()].append(score)

            if (
                self.game_manager.get_drawbag().is_empty()
                and self.game_manager.get_current_turn_player().rack_is_empty()
            ):
                self.end_game()
            else:
                self.game_manager.get_current_turn_player().refill_rack(
                    self.game_manager.get_drawbag()
                )

                self.skip_count = 0
                self.next_turn()
        else:
            self.reset_turn()

    def computer_turn(self):
        """
        Calls the appropriate methods for an AI
        to choose and then play a turn
        """
        if self.game_manager.get_current_turn_player().choose_move():
            self.play_turn()
        else:
            self.skip_turn()

    def reset_turn(self):
        """Reset the current turn"""
        # self.board.set_board(self.saved_board_state)
        # self.game_manager.get_player_list()[0].set_rack(self.saved_rack_state)

        self.game_manager.get_board().reset_blanks()
        self.game_manager.get_current_turn_player().add_tiles(
            self.game_manager.get_board().get_current_turn_tiles()
        )
        self.game_manager.get_board().clear_current_turn_tiles()

        self.update_board_display()
        self.update_rack_display()

        # Clear any held tile
        self.held_tile = None
        self.held_tile_index = -1

    def trade_in(self):
        """Trade in any number (incl. 0) of tiles for new ones and end your turn"""
        self.reset_turn()
        self.trade_in_active = True

    def skip_turn(self):
        """Skips the current turn without playing a word or drawing new tiles"""
        self.skip_count += 1

        if self.skip_count == len(self.game_manager.get_player_list()) * 2:
            self.end_game()
        else:
            self.next_turn()

    def shuffle_rack(self):
        """Shuffles the current player's rack"""
        random.shuffle(self.game_manager.get_current_turn_player().get_rack_tiles())
        self.update_displays()

    def next_turn(self):
        """
        Either schedules a computer turn or allows the
        player to play based on curr_player
        """
        self.trade_in_active = False
        self.tiles_to_trade.clear()
        self.game_manager.next_turn()
        self.update_displays()
        if isinstance(self.game_manager.get_current_turn_player(), AI):
            arcade.schedule_once(lambda _: self.computer_turn(), 0.1)

    def end_game(self):
        """Ends the game"""
        self.update_displays()
        final_scores = self.game_manager.end_game()
        print(final_scores)
        arcade.close_window()

    def update_displays(self):
        """Calls all 3 update methods"""
        self.update_board_display()
        self.update_rack_display()
        self.update_text_display()

    def update_board_display(self):
        """Update the visual representation of the board to match the current board state"""
        # Clear existing board sprites
        self.board_sprites.clear()

        # Create new sprites for each tile on the board
        current_board = self.game_manager.get_board().get_board()
        for row in range(SIZE):
            for col in range(SIZE):
                _tile = current_board[row][col]
                tile = Tile(_tile.letter, _tile.value, _tile.image_path)

                x, y = get_board_position(row, col)
                tile.sprite.center_x = x - 7
                tile.sprite.center_y = y

                self.board_sprites.append(tile.sprite)

    def update_rack_display(self):
        """Update the visual representation of the rack to match the player's rack"""
        # Clear existing rack tiles and positions (except rack graphic)
        while not len(self.rack_sprites) == 0:
            self.rack_sprites.pop()

        if not isinstance(self.game_manager.get_current_turn_player(), AI):
            for i, tile in enumerate(
                self.game_manager.get_current_turn_player().get_rack_tiles()
            ):
                x, y = get_rack_position(i)
                tile.sprite.center_x = x
                tile.sprite.center_y = y
                tile.sprite.scale = 1.2

                if tile.sprite not in self.rack_sprites:
                    self.rack_sprites.append(tile.sprite)

    def update_text_display(self):
        """Update the visual representation of the score and history to match the game state"""
        self.text_objects = []

        turn_text = self.game_manager.get_current_turn_player().get_name() + "'s turn!"

        self.text_objects = [
            arcade.Text(
                turn_text,
                BACKGROUND_COORDS["turn_display"][0],
                BACKGROUND_COORDS["turn_display"][1] - 75,
                arcade.color.WHITE,
                22,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ),
            arcade.Text(
                "Scoreboard",
                BACKGROUND_COORDS["scoreboard"][0] - 70,
                BACKGROUND_COORDS["scoreboard"][1] + 240,
                arcade.color.WHITE,
                18,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ),
            arcade.Text(
                "Play Word",
                BUTTON_X,
                self.button_sprites.sprite_list[0].center_y - 6,
                arcade.color.WHITE,
                14,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ),
            arcade.Text(
                "Reset",
                BUTTON_X,
                self.button_sprites.sprite_list[1].center_y - 6,
                arcade.color.WHITE,
                14,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ),
            arcade.Text(
                "Shuffle",
                BUTTON_X,
                self.button_sprites.sprite_list[2].center_y - 6,
                arcade.color.WHITE,
                14,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ),
            arcade.Text(
                "Trade In",
                BUTTON_X,
                self.button_sprites.sprite_list[3].center_y - 6,
                arcade.color.WHITE,
                14,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ),
            arcade.Text(
                "Letter Distribution",
                BACKGROUND_COORDS["letter_dist"][0],
                BACKGROUND_COORDS["letter_dist"][1] + 240,
                arcade.color.WHITE,
                18,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ),
            arcade.Text(
                LETTER_DIST,
                BACKGROUND_COORDS["letter_dist"][0] - 100,
                BACKGROUND_COORDS["letter_dist"][1] + 200,
                arcade.color.WHITE,
                14,
                align="center",
                font_name="Minecraft",
                width=205,
                multiline=True,
            ),
        ]

        turns_shown = 20 // len(self.game_manager.get_player_list())
        offset = 20 * (1 + turns_shown)

        for i, player in enumerate(self.game_manager.get_player_list()):
            self.text_objects.append(
                arcade.Text(
                    f"{player.get_name()}:   {player.get_score()}",
                    BACKGROUND_COORDS["scoreboard"][0] - 140,
                    BACKGROUND_COORDS["scoreboard"][1] + 210 - (offset * i),
                    arcade.color.WHITE,
                    14,
                    font_name="Minecraft",
                )
            )

            for j, score in enumerate(
                reversed(self.game_history[player][-turns_shown:])
            ):
                self.text_objects.append(
                    arcade.Text(
                        f"Turn {len(self.game_history[player]) - j}: +{score}",
                        BACKGROUND_COORDS["scoreboard"][0] + 50,
                        BACKGROUND_COORDS["scoreboard"][1]
                        + 210
                        - (offset * i)
                        - (20 * (j + 1)),
                        arcade.color.WHITE,
                        12,
                        font_name="Minecraft",
                    )
                )
