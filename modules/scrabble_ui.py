"""Module containing the definition for a ScrabbleUI object"""

from .config import (
    arcade,
    SIZE,
    TILE_SIZE,
    TILE_GAP,
    BORDER_Y,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    BOARD_START_X,
    BOARD_START_Y,
    BOARD_SIZE,
    RACK_TILE_SPACING,
    BUTTON_X,
    BOARD_CENTER_X,
    BOARD_CENTER_Y,
)
from .tile import Tile
from .board import EMPTY_TILES
from .utils import to_coords
from .game_manager import GameManager
from .ai import AI


class ScrabbleUI(arcade.View):
    """
    Class representing the Scrabble UI
    """

    def __init__(self):
        super().__init__()

        # TODO: should implement a difficulty select on start screen
        # self.DIFFICULTY = "hard"

        # TODO: optional but can implement a background select on start screen
        bg = "gray"
        backgrounds = {
            "gray": "./assets/images/gray.jpg",
            "starry": "./assets/images/starry.jpeg",
            "mountains": "./assets/images/mountains.jpeg",
        }

        # initialize game manager
        self.game_manager = GameManager([("ai", "words", 1), ("ai", "longest", 3)])

        # For displaying the game history
        self.game_history = {}

        for player in self.game_manager.get_player_list():
            self.game_history[player] = []

        # for determining the current held tile
        self.held_tile = None
        self.held_tile_index = None

        self.bingo = False
        self.trade_in_active = False
        self.tiles_to_trade = []

        # For displaying pop up messages
        self.popup = arcade.SpriteList()

        self.box = arcade.Sprite("./assets/images/turn_display.png")
        self.box.size = (WINDOW_WIDTH // 3, WINDOW_HEIGHT // 3)
        self.box.center_x = BOARD_CENTER_X
        self.box.center_y = BOARD_CENTER_Y

        self.popup.append(self.box)

        self.done_button = arcade.SpriteList()
        self._done_button = arcade.Sprite("./assets/images/trade_in_button.png")
        self._done_button.center_x = BOARD_CENTER_X
        self._done_button.center_y = BOARD_CENTER_Y - 100
        self.done_button.append(self._done_button)

        # Prompt user to select a letter for the blank tile
        self.blank_tile_prompt = False
        self.blank_tile_position = None

        # Create a temporary text input
        self.letter_input = ""
        self.text_input_active = False

        """ Sprites creation for graphics """
        # displays the current board state
        self.board_sprites: arcade.SpriteList = arcade.SpriteList()

        # displays player's rack
        self.rack_sprites: arcade.SpriteList = arcade.SpriteList()

        # displays buttons
        self.button_sprites: arcade.SpriteList = arcade.SpriteList()

        reset_button = arcade.Sprite(
            "./assets/images/reset_button.png",
            center_x=BUTTON_X,
            center_y=BORDER_Y * 0.8,
        )

        trade_in_button = arcade.Sprite(
            "./assets/images/trade_in_button.png",
            center_x=BUTTON_X,
            center_y=BORDER_Y * 0.5,
        )

        play_word_button = arcade.Sprite(
            "./assets/images/play_word_button.png",
            center_x=BUTTON_X,
            center_y=BORDER_Y * 1.1,
        )

        self.button_sprites.append(play_word_button)
        self.button_sprites.append(reset_button)
        self.button_sprites.append(trade_in_button)

        # displays background sprites
        self.background_sprites: arcade.SpriteList = arcade.SpriteList()

        window_background = arcade.Sprite(
            backgrounds[bg], center_x=WINDOW_WIDTH // 2, center_y=WINDOW_HEIGHT // 2
        )
        window_background.size = (WINDOW_WIDTH, WINDOW_HEIGHT)

        board_background = arcade.Sprite(
            "./assets/images/background.png",
            center_x=BOARD_CENTER_X - 7,
            center_y=BOARD_CENTER_Y,
        )
        board_background.size = (BOARD_SIZE * 1.15, BOARD_SIZE * 1.15)

        turn_display = arcade.Sprite(
            "./assets/images/turn_display.png",
            center_x=WINDOW_WIDTH * 0.13,
            center_y=WINDOW_HEIGHT + 30,
        )

        scoreboard_background = arcade.Sprite(
            "./assets/images/scoreboard_background.png",
            center_x=WINDOW_WIDTH * 0.13,
            center_y=WINDOW_HEIGHT * 0.58,
        )

        letter_dist_background = arcade.Sprite(
            "./assets/images/scoreboard_background.png",
            center_x=WINDOW_WIDTH * 0.87,
            center_y=WINDOW_HEIGHT * 0.58,
        )

        rack_background = arcade.Sprite("./assets/images/rack.png")
        rack_background.center_x = WINDOW_WIDTH // 2
        rack_background.center_y = BORDER_Y * 0.8

        self.background_sprites.append(window_background)
        self.background_sprites.append(board_background)
        self.background_sprites.append(turn_display)
        self.background_sprites.append(scoreboard_background)
        self.background_sprites.append(letter_dist_background)
        self.background_sprites.append(rack_background)

        # Displays all text
        self.text_objects = []
        arcade.load_font("./assets/Minecraft.ttf")

        self.update_displays()
        self.next_turn()

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """

        # Make tiles move up slightly to indicate the player hovering over them
        for i, sprite in enumerate(self.rack_sprites):
            if sprite.collides_with_point((x, y)):
                new_y = self.get_rack_position(i)[1] + 20
                sprite.center_y = new_y
            else:
                _, original_y = self.get_rack_position(i)
                sprite.center_y = original_y

        image_names = ["play_word_button", "reset_button", "trade_in_button"]
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
                        self.trade_in()
        elif self._done_button.collides_with_point((x, y)):
            self.game_manager.get_current_turn_player().refill_rack(
                self.game_manager.get_drawbag()
            )
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
                        self.blank_tile_prompt = True
                        self.blank_tile_position = (row, col)

                        # Create a temporary text input
                        self.letter_input = ""
                        self.text_input_active = True

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
                if self.box.collides_with_point((x, y)) and self.held_tile:
                    self.game_manager.get_current_turn_player().get_rack().remove_tile(
                        self.held_tile
                    )
                    self.tiles_to_trade.append(self.held_tile)
                    self.update_rack_display()
                    placed = True

            # Allow for dragging tiles onto one another in the rack to swap their positions
            if not placed:
                for i, rack_tile in enumerate(
                    self.game_manager.get_current_turn_player().get_rack_tiles()
                ):
                    if (
                        rack_tile != self.held_tile
                        and rack_tile.sprite.collides_with_point((x, y))
                    ):
                        self.swap_rack_tiles(self.held_tile_index, i)
                        placed = True
                        break

            # If the tile is not dragged to a valid spot on the board, reset it back to rack
            if not placed and self.held_tile_index is not None:
                original_x, original_y = self.get_rack_position(self.held_tile_index)
                self.held_tile.sprite.center_x = original_x
                self.held_tile.sprite.center_y = original_y
                self.held_tile.sprite.scale = 1.2

            self.held_tile = None
            self.held_tile_index = None

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
        # Draw blank tile prompt if active
        if hasattr(self, "text_input_active") and self.text_input_active:
            self.popup.draw()
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
            self.popup.draw()
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
                "Click anywhere on screen to continue",
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
            self.popup.draw()
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

    def on_key_press(self, symbol, modifiers):
        """
        Handle keyboard input for blank tile letter selection
        """
        if hasattr(self, "text_input_active") and self.text_input_active:
            if 97 <= symbol <= 122:
                letter = chr(symbol).lower()
                row, col = self.blank_tile_position

                new_tile = Tile(letter, 0, f"./assets/images/{letter}.png")
                self.game_manager.get_board().update_tile(row, col, new_tile)

                self.update_board_display()

                self.text_input_active = False
                del self.blank_tile_prompt
                del self.blank_tile_position
                return

        if self.trade_in_active:
            if symbol == arcade.key.ESCAPE:
                self.trade_in_active = False
                self.game_manager.get_current_turn_player().add_tiles(
                    self.tiles_to_trade
                )
                self.tiles_to_trade.clear()
                self.reset_turn()
                return

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that

    def play_turn(self):
        """
        Confirms the played turn's legality and performs
        the logic needed to finish a played turn
        """
        is_valid, words = self.game_manager.get_board().play_turn()
        if is_valid:
            score = sum(words.values())

            self.game_manager.get_current_turn_player().add_score(score)

            self.game_manager.get_current_turn_player().refill_rack(
                self.game_manager.get_drawbag()
            )

            for word, points in words.items():
                self.game_history[self.game_manager.get_current_turn_player()].append(
                    (word, points)
                )

            self.next_turn()
        else:
            self.reset_turn()

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
        self.held_tile_index = None

    def trade_in(self):
        """Trade in any number (incl. 0) of tiles for new ones and end your turn"""
        self.reset_turn()
        self.trade_in_active = True

    def computer_turn(self):
        """
        Calls the appropriate methods for an AI
        to choose and then play a turn
        """
        if self.game_manager.get_current_turn_player().choose_move():
            self.play_turn()
        else:
            self.next_turn()

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

    def swap_rack_tiles(self, index1, index2):
        """Swap two tiles in the player's rack and update the display"""
        # Swap tiles in the player's rack
        rack = self.game_manager.get_current_turn_player().get_rack_tiles()
        rack[index1], rack[index2] = rack[index2], rack[index1]

        # Update visuals
        self.update_rack_display()

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

                x, y = self.get_board_position(row, col)
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
                x, y = self.get_rack_position(i)
                tile.sprite.center_x = x
                tile.sprite.center_y = y
                tile.sprite.scale = 1.2

                if tile.sprite not in self.rack_sprites:
                    self.rack_sprites.append(tile.sprite)

    def update_text_display(self):
        """Update the visual representation of the score and history to match the game state"""
        self.text_objects = []

        letter_dist = "\
A - 9     J - 1     S - 4  \
--------------------------- \
    B - 2     K - 1     T - 6 \
--------------------------- \
    C - 2     L - 4     U - 4 \
--------------------------- \
    D - 4     M - 2     V - 2 \
--------------------------- \
    E - 12    N - 6     W - 2 \
--------------------------- \
    F - 2     O - 8     X - 1 \
--------------------------- \
    G - 3     P - 2     Y - 2 \
--------------------------- \
    H - 2     Q - 1     Z - 1 \
--------------------------- \
    I - 9   R - 6   Blank - 2"

        offset = 20 * len(self.game_history[self.game_manager.get_player_list()[0]])

        turn_text = self.game_manager.get_current_turn_player().get_name() + "'s turn!"

        self.text_objects = [
            arcade.Text(
                turn_text,
                self.background_sprites[2].center_x,
                self.background_sprites[2].center_y - 75,
                arcade.color.WHITE,
                22,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ),
            arcade.Text(
                "Scoreboard",
                self.background_sprites[3].center_x - 70,
                self.background_sprites[3].center_y + 240,
                arcade.color.WHITE,
                18,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ),
            arcade.Text(
                f"\
{self.game_manager.get_player_list()[0].get_name()}: \
{self.game_manager.get_player_list()[0].get_score()}",
                self.background_sprites[3].center_x - 140,
                self.background_sprites[3].center_y + 200,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                f"\
{self.game_manager.get_player_list()[1].get_name()}: \
{self.game_manager.get_player_list()[1].get_score()}",
                self.background_sprites[3].center_x - 140,
                (self.background_sprites[3].center_y + 160) - offset,
                arcade.color.WHITE,
                14,
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
                "Trade In",
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
                "Letter Distribution",
                self.background_sprites[4].center_x,
                self.background_sprites[4].center_y + 240,
                arcade.color.WHITE,
                18,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft",
            ),
            arcade.Text(
                letter_dist,
                self.background_sprites[4].center_x - 100,
                self.background_sprites[4].center_y + 200,
                arcade.color.WHITE,
                14,
                align="center",
                font_name="Minecraft",
                width=205,
                multiline=True,
            ),
        ]

        # For displaying previous turn results
        if len(self.game_history[self.game_manager.get_player_list()[0]]) > 10:
            self.game_history[self.game_manager.get_player_list()[0]].pop(0)
        if len(self.game_history[self.game_manager.get_player_list()[1]]) > 10:
            self.game_history[self.game_manager.get_player_list()[1]].pop(0)

        for i in range(len(self.game_history[self.game_manager.get_player_list()[0]])):
            turn = self.game_history[self.game_manager.get_player_list()[0]][i]
            word, score = turn[0], turn[1]
            self.text_objects.append(
                arcade.Text(
                    f"+{score}        {word}",
                    self.background_sprites[3].center_x - 100,
                    (self.background_sprites[3].center_y + 180) - 20 * i,
                    arcade.color.WHITE,
                    12,
                    font_name="Minecraft",
                )
            )

        for i in range(len(self.game_history[self.game_manager.get_player_list()[1]])):
            turn = self.game_history[self.game_manager.get_player_list()[1]][i]
            word, score = turn[0], turn[1]
            self.text_objects.append(
                arcade.Text(
                    f"+{score}        {word}",
                    self.background_sprites[3].center_x - 100,
                    (self.background_sprites[3].center_y + 140) - offset - 20 * i,
                    arcade.color.WHITE,
                    12,
                    font_name="Minecraft",
                )
            )

    def get_board_position(self, row, col):
        """Calculate the screen position for a board tile at the given row and column."""
        x = col * (TILE_SIZE + TILE_GAP) + BOARD_START_X
        y = (SIZE - 1 - row) * (TILE_SIZE + TILE_GAP) + BOARD_START_Y
        return x, y

    def get_rack_position(self, tile_index):
        """Calculate the screen position for a rack tile at the given index."""
        x = BOARD_START_X + (RACK_TILE_SPACING * tile_index)
        y = self.background_sprites[5].center_y
        return x, y
