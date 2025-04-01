""" Module containing the definition for a ScrabbleUI object """

from .config import (arcade, ROWS, COLS, TILE_SIZE, TILE_GAP,
                     BORDER_X, BORDER_Y, WINDOW_WIDTH, BOARD_SIZE)
from .tile import Tile
from .drawbag import Drawbag
from .player import Player
from .board import Board
from .utils import from_coords, to_coords
from .game_manager import GameManager

class ScrabbleUI(arcade.View):
    """
    Class representing the Scrabble UI
    """
    def __init__(self):
        super().__init__()

        # Position constants for dynamic graphics
        self.board_start_x = BORDER_X
        self.board_start_y = BORDER_Y * 1.5
        self.rack_start_x = int(WINDOW_WIDTH / 3.25)
        self.rack_tile_spacing = TILE_SIZE * 2.5
        self.button_x = WINDOW_WIDTH - BORDER_X * 0.6
        self.board_center_x = 7 * (TILE_SIZE + TILE_GAP) + BORDER_X
        self.board_center_y = (ROWS - 8) * (TILE_SIZE + TILE_GAP) + BORDER_Y * 1.5

        self.background_color = arcade.color.GRAY

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

        """ Sprites creation for graphics """
        # displays the current board state
        self.board_sprites: arcade.SpriteList = arcade.SpriteList()
        for row in range(ROWS):
            for col in range(COLS):
                _tile = self.board.get_board()[row][col]
                tile = Tile(_tile.letter, _tile.value, _tile.image_path)

                x, y = self.get_board_position(row, col)
                tile.sprite.center_x = x
                tile.sprite.center_y = y

                self.board_sprites.append(tile.sprite)

        # displays player's rack
        self.rack_sprites: arcade.SpriteList = arcade.SpriteList()
        self.rack_graphic = arcade.Sprite("./assets/images/rack.png")
        self.rack_graphic.center_x = int(WINDOW_WIDTH / 2)
        self.rack_graphic.center_y = BORDER_Y * 0.8
        self.rack_sprites.append(self.rack_graphic)

        self.update_rack_display()

        # displays buttons
        self.button_sprites: arcade.SpriteList = arcade.SpriteList()

        # Reset button
        self.reset_button = arcade.Sprite("./assets/images/reset_button.png")
        self.reset_button.center_x = self.button_x
        self.reset_button.center_y = BORDER_Y * 0.8

        # Trade-in button
        self.trade_in_button = arcade.Sprite("./assets/images/trade_in_button.png")
        self.trade_in_button.center_x = self.button_x
        self.trade_in_button.center_y = BORDER_Y * 0.5

        # Play word button
        self.play_word_button = arcade.Sprite("./assets/images/play_word_button.png")
        self.play_word_button.center_x = self.button_x
        self.play_word_button.center_y = BORDER_Y * 1.1

        self.button_sprites.append(self.trade_in_button)
        self.button_sprites.append(self.reset_button)
        self.button_sprites.append(self.play_word_button)

        # displays miscellaneous graphics
        self.other_sprites: arcade.SpriteList = arcade.SpriteList()
        self.board_background = arcade.Sprite('./assets/images/background.png')
        self.board_background.size = (BOARD_SIZE * 1.15, BOARD_SIZE * 1.15)
        self.board_background.center_x = self.board_center_x
        self.board_background.center_y = self.board_center_y
        self.other_sprites.append(self.board_background)

    def get_board_position(self, row, col):
        """ Calculate the screen position for a board tile at the given row and column."""
        x = col * (TILE_SIZE + TILE_GAP) + self.board_start_x
        y = (ROWS - 1 - row) * (TILE_SIZE + TILE_GAP) + self.board_start_y
        return x, y

    def get_rack_position(self, tile_index):
        """ Calculate the screen position for a rack tile at the given index. """
        x = self.rack_start_x + (self.rack_tile_spacing * tile_index)
        y = self.rack_graphic.center_y
        return x, y

    def update_rack_display(self):
        """ Update the visual representation of the rack to match the player's rack """
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

    def swap_rack_tiles(self, index1, index2):
        """ Swap two tiles in the player's rack and update the display """
        # Swap tiles in the player's rack
        rack = self.player.get_rack()
        rack[index1], rack[index2] = rack[index2], rack[index1]

        # Update visuals
        self.update_rack_display()

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that

    def reset_turn(self):
        """ 
        Reset the game to its state at beginning of turn 
        
        For when user hits reset button or when an invalid word is played
        """
        #TODO: implement

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
        self.rack_sprites.draw()
        self.button_sprites.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
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
                    #TODO: implement tile trade in
                    pass
                elif button_sprite == self.play_word_button:
                    #TODO: implement functionality for playing words
                    pass

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

                    letter = self.held_tile.letter
                    value = self.held_tile.value
                    image_path = self.held_tile.image_path

                    new_tile = Tile(letter, value, image_path)
                    self.board.update_tile(row, col, new_tile)

                    board_sprite.texture = arcade.load_texture(image_path)

                    # Remove the tile from player's rack
                    self.player.rack.remove_tile(self.player.get_rack()[self.held_tile_index])

                    # Update the rack display
                    self.update_rack_display()

                    placed = True
                    break

            # Allow for dragging tiles onto one another in the rack to swap their positions
            if not placed:
                for i, rack_tile in enumerate(self.rack_tiles):
                    if rack_tile != self.held_tile and rack_tile.sprite.collides_with_point((x, y)):
                        self.swap_rack_tiles(self.held_tile_index, i)
                        placed = True
                        break

            # If the tile is not dragged to a valid spot on the board, reset it back to rack
            if (not placed and self.held_tile_index is not None
                and self.held_tile_index < len(self.original_rack_positions)):
                original_x, original_y = self.original_rack_positions[self.held_tile_index]
                self.held_tile.sprite.center_x = original_x
                self.held_tile.sprite.center_y = original_y
                self.held_tile.sprite.scale = 1.2

            self.held_tile = None
            self.held_tile_index = None
