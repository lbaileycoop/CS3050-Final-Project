"""Module containing the definition for a ScrabbleUI object"""

from .config import (
    arcade,
    ROWS,
    COLS,
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
        self.game_manager = GameManager([("human", "Player"), ("ai", "Computer")])

        # For displaying the game history
        self.game_history = {}

        for player in self.game_manager.get_player_list():
            self.game_history[player] = []

        # for determining the current held tile
        self.held_tile = None
        self.held_tile_index = None

        """ Sprites creation for graphics """
        # displays the current board state
        self.board_sprites: arcade.SpriteList = arcade.SpriteList()

        # displays player's rack
        self.rack_sprites: arcade.SpriteList = arcade.SpriteList()

        rack_graphic = arcade.Sprite("./assets/images/rack.png")
        rack_graphic.center_x = WINDOW_WIDTH // 2
        rack_graphic.center_y = BORDER_Y * 0.8

        self.rack_sprites.append(rack_graphic)

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

        # displays miscellaneous graphics
        self.other_sprites: arcade.SpriteList = arcade.SpriteList()

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

        self.other_sprites.append(window_background)
        self.other_sprites.append(board_background)
        self.other_sprites.append(turn_display)
        self.other_sprites.append(scoreboard_background)
        self.other_sprites.append(letter_dist_background)

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
        for idx in range(1, len(self.rack_sprites)):
            if self.rack_sprites[idx].collides_with_point((x, y)):
                new_y = self.get_rack_position(idx)[1] + 20
                self.rack_sprites[idx].center_y = new_y
            else:
                _, original_y = self.get_rack_position(idx)
                self.rack_sprites[idx].center_y = original_y

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
            if self.other_sprites[1].collides_with_point((x, y)):
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

            # Check if a button was clicked
            for i, sprite in enumerate(self.button_sprites):
                if sprite.collides_with_point((x, y)):
                    if i == 0:
                        self.play_turn()
                    elif i == 1:
                        self.reset_turn()
                    elif i == 2:
                        self.trade_in()

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
                    if self.game_manager.get_board().get_tile_at(
                        row, col
                    ) not in EMPTY_TILES or isinstance(
                        self.game_manager.get_current_turn_player(), AI
                    ):
                        continue

                    new_tile = Tile.copy(self.held_tile)

                    if new_tile.letter == "":
                        # TODO: implement function to take input for new_letter
                        new_tile.set_blank("a")
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
        self.other_sprites.draw()
        self.board_sprites.draw()
        self.button_sprites.draw()

        for text_object in self.text_objects:
            text_object.draw()

        self.rack_sprites.draw()

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

            self.game_manager.next_turn()
            self.update_displays()
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
        # TODO

    def computer_turn(self):
        """
        Calls the appropriate methods for an AI
        to choose and then play a turn
        """
        self.game_manager.get_current_turn_player().choose_move()

        self.play_turn()

        # self.board.reset_current_turn_tiles()
        # curr_player = self.game_manager.get_current_turn_player()
        # curr_player.add_score(sum(words.values()))

        # curr_player.refill_rack(self.game_manager.get_drawbag())
        # self.update_rack_display()

        # self.game_manager.next_turn()

        # for word, points in words.items():
        #     self.game_history[curr_player].append((word, points))
        # self.update_text_display()
        # self.update_board_display()

        # letters = ""
        # num_free_letters = 0
        # for tile in computer_player_object.get_rack():
        #     if tile.letter == "":
        #         num_free_letters += 1
        #     else:
        #         letters += tile.letter

        # possible_words = get_possible_words(letters, num_free_letters)
        # # TODO: For now just determining word quality by length, but should be changed to score
        # sorted_possible_words = sorted(possible_words, key=len)

        # word_to_play = ""
        # if difficulty == "easy":
        #     word_to_play = sorted_possible_words[0]
        # elif difficulty == "medium":
        #     word_to_play = sorted_possible_words[len(sorted_possible_words) // 2]
        # elif difficulty == "hard":
        #     word_to_play = sorted_possible_words[len(sorted_possible_words) - 1]
        # else:
        #     word_to_play = sorted_possible_words[
        #         random.randint(0, len(sorted_possible_words) - 1)
        #     ]

        # print(word_to_play)

        # # get corresponding tiles
        # tiles_to_play = []
        # for ch in word_to_play:
        #     for i, tile in enumerate(computer_player_object.get_rack()):
        #         if tile.letter == ch:
        #             tiles_to_play.append(computer_player_object.get_rack().pop(i))
        #             break

        # # TODO: implement actual logic for places the computer should play,
        # # for now, just places them where there is empty space
        # for row in range(15):
        #     for col in range(15):
        #         if (
        #             tiles_to_play
        #             and self.game_manager.get_board().get_board()[row][col].letter
        #             == ORIGINAL_BOARD[row][col].letter
        #         ):
        #             tile_to_play = tiles_to_play.pop(0)
        #             self.game_manager.get_board().update_tile(row, col, tile_to_play)

        # # play the turn
        # word, is_valid, score = self.game_manager.get_board().validate_turn()

        # if is_valid:
        #     computer_player_object.add_score(score)

        #     # Refill computer rack
        #     computer_player_object.refill_rack(drawbag)

        #     game_manager.next_turn()

        #     self.game_history[computer_player_object].append((word, score))
        #     self.update_text_display()
        #     self.update_board_display()

        #     self.save_game_state()
        # else:
        #     self.reset_turn()
        #     print("ERROR in computer turn")

    def next_turn(self):
        """
        Either schedules a computer turn or allows the
        player to play based on curr_player
        """
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
        for _ in range(1, len(self.rack_sprites)):
            self.rack_sprites.pop(1)

        for i, tile in enumerate(
            self.game_manager.get_current_turn_player().get_rack_tiles()
        ):
            # _tile = self.game_manager.get_player_list()[0].get_rack_tiles()[i]
            # tile = Tile(_tile.letter, _tile.value, _tile.image_path, scale=1.2)

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
A - 9        N - 6 \
------------------- \
B - 2        O - 8 \
------------------- \
C - 2        P - 2 \
------------------- \
D - 4        Q - 1 \
------------------- \
E - 12      R - 6 \
------------------- \
F - 2        S - 4 \
------------------- \
G - 3        T - 6 \
------------------- \
H - 2        U - 4 \
------------------- \
I - 9         V - 2 \
------------------- \
J - 1         W - 2 \
------------------- \
K - 1         X - 1 \
------------------- \
L - 4        Y - 2 \
------------------- \
M - 2        Z - 1"

        offset = 20 * len(
            self.game_history[self.game_manager.get_current_turn_player()]
        )

        turn_text = self.game_manager.get_current_turn_player().get_name() + "'s turn!"

        self.text_objects = [
            arcade.Text(
                turn_text,
                self.other_sprites[2].center_x - 190,
                self.other_sprites[2].center_y - 75,
                arcade.color.WHITE,
                22,
                380,
                "center",
                "Minecraft",
            ),
            arcade.Text(
                "Scoreboard",
                self.other_sprites[3].center_x - 70,
                self.other_sprites[3].center_y + 240,
                arcade.color.WHITE,
                18,
                font_name="Minecraft",
            ),
            arcade.Text(
                f"Player: {self.game_manager.get_player_list()[0].get_score()}",
                self.other_sprites[3].center_x - 140,
                self.other_sprites[3].center_y + 200,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                f"Computer: {self.game_manager.get_player_list()[1].get_score()}",
                self.other_sprites[3].center_x - 140,
                (self.other_sprites[3].center_y + 160) - offset,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                "Play Word",
                BUTTON_X - 42,
                self.button_sprites.sprite_list[0].center_y - 6,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                "Reset",
                BUTTON_X - 25,
                self.button_sprites.sprite_list[1].center_y - 6,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                "Trade In",
                BUTTON_X - 42,
                self.button_sprites.sprite_list[2].center_y - 6,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
            ),
            arcade.Text(
                "Letter Distribution",
                self.other_sprites[4].center_x - 100,
                self.other_sprites[4].center_y + 240,
                arcade.color.WHITE,
                18,
                font_name="Minecraft",
            ),
            arcade.Text(
                letter_dist,
                self.other_sprites[4].center_x - 70,
                self.other_sprites[4].center_y + 200,
                arcade.color.WHITE,
                14,
                font_name="Minecraft",
                width=140,
                multiline=True,
            ),
        ]

        # For displaying previous turn results
        for i in range(len(self.game_history[self.game_manager.get_player_list()[0]])):
            turn = self.game_history[self.game_manager.get_player_list()[0]][i]
            word, score = turn[0], turn[1]
            self.text_objects.append(
                arcade.Text(
                    f"+{score}        {word}",
                    self.other_sprites[3].center_x - 100,
                    (self.other_sprites[3].center_y + 180) - 20 * i,
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
                    self.other_sprites[3].center_x - 100,
                    (self.other_sprites[3].center_y + 140) - offset - 20 * i,
                    arcade.color.WHITE,
                    12,
                    font_name="Minecraft",
                )
            )

    def get_board_position(self, row, col):
        """Calculate the screen position for a board tile at the given row and column."""
        x = col * (TILE_SIZE + TILE_GAP) + BOARD_START_X
        y = (ROWS - 1 - row) * (TILE_SIZE + TILE_GAP) + BOARD_START_Y
        return x, y

    def get_rack_position(self, tile_index):
        """Calculate the screen position for a rack tile at the given index."""
        x = BOARD_START_X + (RACK_TILE_SPACING * tile_index)
        y = self.rack_sprites[0].center_y
        return x, y
