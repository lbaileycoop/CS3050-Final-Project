from typing import Tuple
import arcade
from tile import Tile, WINDOW_WIDTH, WINDOW_HEIGHT, BOARD_SIZE, TILE_SIZE
from drawbag import Drawbag
from player import Player
from board import Board

# Additional constants
WINDOW_TITLE = "Scrabble"
ROWS = 15
COLS = 15
TILE_GAP = TILE_SIZE * 0.1
DOCK_SIZE_X = BOARD_SIZE
DOCK_SIZE_Y = int(BOARD_SIZE / 4)
BORDER_X = (WINDOW_WIDTH - BOARD_SIZE) // 2
BORDER_Y = (WINDOW_HEIGHT - BOARD_SIZE) // 2

class StartScreen(arcade.View):
    """A simple start screen for the Scrabble game."""
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.DARK_SLATE_GRAY  # Fallback color if image fails
        # Load the background image
        try:
            self.background = arcade.load_texture("./assets/Background.png")
        except FileNotFoundError:
            self.background = None  # Handle case where image is missing
            print("Warning: Could not load start_screen.png. Using solid background color.")

    def on_draw(self):
        """Render the start screen."""
        self.clear()
        # Draw the background image if it exists
        if self.background:
            arcade.draw_texture_rectangle(
                WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,  # Center of the screen
                WINDOW_WIDTH, WINDOW_HEIGHT,          # Stretch to fill the window
                self.background
            )
        # Draw the title
        arcade.draw_text(
            "Scrabble",
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 + 50,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center"
        )
        # Draw instructions
        arcade.draw_text(
            "Press any key to start",
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 - 50,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        """Switch to the Scrabble game when any key is pressed."""
        game_view = ScrabbleUI()
        self.window.show_view(game_view)

class ScrabbleUI(arcade.View):
    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.BISTRE_BROWN
        self.held_tile = None
        self.held_tile_index = None
        self.drawbag = Drawbag()
        self.player = Player("You", self.drawbag)
        self.logic_board = Board()
        self.sprite_board = self.logic_board.get_board()

        # displays the current board state
        self.board: arcade.SpriteList = arcade.SpriteList()
        for row in range(ROWS):
            for col in range(COLS):
                _tile = self.sprite_board[row][col]
                tile = Tile(_tile.letter, _tile.value, _tile.image_path)

                tile.sprite.center_x = col * (TILE_SIZE + TILE_GAP) + BORDER_X
                tile.sprite.center_y = (ROWS - 1 - row) * (TILE_SIZE + TILE_GAP) + BORDER_Y*1.5

                self.board.append(tile.sprite)

        # displays player's rack
        self.rack: arcade.SpriteList = arcade.SpriteList()
        rack_graphic = arcade.Sprite("./assets/rack.png")
        rack_graphic.center_x = int(WINDOW_WIDTH / 2)
        rack_graphic.center_y = BORDER_Y*0.8
        self.rack.append(rack_graphic)

        self.rack_tiles = []
        self.original_rack_positions = []

        # adds tiles to the player's rack
        for i in range(self.player.rack.len_rack()):
            _tile = self.player.get_rack()[i]
            tile = Tile(_tile.letter, _tile.value, _tile.image_path)

            tile.sprite.center_x = int(WINDOW_WIDTH / 3.25) + (TILE_SIZE *2.5* i)
            tile.sprite.center_y = rack_graphic.center_y

            self.rack.append(tile.sprite)
            self.rack_tiles.append(tile.sprite)
            self.original_rack_positions.append((tile.sprite.center_x, tile.sprite.center_y))

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def on_draw(self):
        """Render the screen."""
        self.clear()
        self.board.draw()
        self.rack.draw()

    def to_coords(self, index: int) -> Tuple[int, int]:
        """Returns the x and y values of a tile based on the 1-d index"""
        return (index % COLS, (index // COLS))

    def from_coords(self, x: int, y: int) -> Tuple[int, int]:
        """Returns the 1-d index of a tile based on the x and y values"""
        return x + ((ROWS - y) * COLS)

    def on_update(self, delta_time):
        """All the logic to move, and the game logic goes here."""
        pass

    def on_key_press(self, key, key_modifiers):
        """Called whenever a key on the keyboard is pressed."""
        pass

    def on_key_release(self, key, key_modifiers):
        """Called whenever the user lets off a previously pressed key."""
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """Called whenever the mouse moves."""
        if self.held_tile:
            self.held_tile.center_x = x
            self.held_tile.center_y = y

    def on_mouse_press(self, x, y, button, key_modifiers):
        """Called when the user presses a mouse button."""
        for i, tile in enumerate(self.rack_tiles):
            if tile.collides_with_point((x, y)):
                self.held_tile = tile
                self.held_tile_index = i
                break

    def on_mouse_release(self, x, y, button, key_modifiers):
        """Called when a user releases a mouse button."""
        if self.held_tile:
            placed = False

            # If a tile is dropped over a space on the board, update the board position to that tile
            for i, board_sprite in enumerate(self.board):
                if board_sprite.collides_with_point((x, y)):
                    col, row = self.to_coords(i)

                    letter = self.player.get_rack()[self.held_tile_index].letter
                    value = self.player.get_rack()[self.held_tile_index].value
                    image_path = self.player.get_rack()[self.held_tile_index].image_path

                    new_tile = Tile(letter, value, image_path)

                    self.logic_board.update_tile(col, row, new_tile)

                    board_sprite.texture = arcade.load_texture(image_path)

                    # Remove the played tile from the user's rack
                    self.player.rack.remove_tile(self.player.get_rack()[self.held_tile_index])

                    self.rack.remove(self.held_tile)
                    self.rack_tiles.remove(self.held_tile)
                    self.original_rack_positions.pop(self.held_tile_index)

                    placed = True
                    break

            # If the tile is not dragged to a valid spot on the board, reset it back to rack
            if not placed and self.held_tile_index is not None:
                original_x, original_y = self.original_rack_positions[self.held_tile_index]
                self.held_tile.center_x = original_x
                self.held_tile.center_y = original_y

            self.held_tile = None
            self.held_tile_index = None