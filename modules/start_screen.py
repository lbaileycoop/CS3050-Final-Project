"""Module containing the definition for a StartScreen object"""

import arcade
from .config import arcade, WINDOW_WIDTH, WINDOW_HEIGHT
from .scrabble_ui import ScrabbleUI


class StartScreen(arcade.View):
    """A simple start screen for the Scrabble game."""

    def __init__(self):
        super().__init__()
        self.background_color = (
            arcade.color.DARK_SLATE_GRAY
        )  # Fallback color if image fails
        # Load the background image
        try:
            self.background = arcade.Sprite(
                "./assets/images/start_background.png",
                center_x=WINDOW_WIDTH / 2,
                center_y=WINDOW_HEIGHT / 2,
                scale=1.2,
            )
        except FileNotFoundError:
            self.background = None  # Handle case where image is missing
            print(
                "Warning: Could not load start_screen.png. Using solid background color."
            )

        self.sprites: arcade.SpriteList = arcade.SpriteList()

        self.sprites.append(self.background)

        title_text = arcade.create_text_sprite("Scrabble", arcade.color.WHITE, 50)
        title_text.center_x = WINDOW_WIDTH / 2
        title_text.center_y = WINDOW_HEIGHT / 2 + 50
        self.sprites.append(title_text)

        start_text = arcade.create_text_sprite(
            "Press any key to start", arcade.color.WHITE, 20
        )
        start_text.center_x = WINDOW_WIDTH / 2
        start_text.center_y = WINDOW_HEIGHT / 2 - 50
        self.sprites.append(start_text)

    def on_draw(self):
        """Render the start screen."""
        self.clear()

        self.sprites.draw()

    def on_key_press(self, symbol, modifiers):
        """Switch to the Scrabble game when any key is pressed."""
        self.start_game()

    def on_mouse_press(self, x, y, button, modifiers):
        self.start_game()

    def start_game(self):
        game_view = ScrabbleUI()
        self.window.show_view(game_view)
