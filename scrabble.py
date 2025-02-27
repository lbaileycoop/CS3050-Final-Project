import arcade

WINDOW_WIDTH = 950
WINDOW_HEIGHT = 950
WINDOW_TITLE = "Scrabble"

ROWS = 15
COLS = 15

TILE_SIZE = 45
TILE_GAP = 5
BORDER = 125

BASE_TILE = './assets/blank.png'

class ScrabbleUI(arcade.View):
    def __init__(self):
        super().__init__();

        self.background_color = arcade.color.BISTRE_BROWN

        # Holds the current board state, empty tiles are initialized as None
        self.board: arcade.SpriteList = arcade.SpriteList()
        for i in range(ROWS * COLS):
            tile = Tile(' ', 0, True)
            coords = self.to_coords(i)
            tile.sprite.center_x = coords[0] * (TILE_SIZE + TILE_GAP) + BORDER
            tile.sprite.center_y = coords[1] * (TILE_SIZE + TILE_GAP) + BORDER

            tile.textSprite.center_x = tile.sprite.center_x
            tile.textSprite.center_y = tile.sprite.center_y

            self.board.append(tile.sprite)
            self.board.append(tile.textSprite)
        

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass


    def on_draw(self):
        """
        Render the screen.
        """


        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # Call draw() on all your sprite lists below

        
        self.board.initialize()
        self.board.draw()


    def to_coords(self, index: int) -> (int, int):
        """Returns the x and y values of a tile based on the 1-d index"""
        return (index % COLS, (index // COLS))

    def from_coords(self, x: int, y: int) -> (int, int):
        """Returns the 1-d index of a tile based on the x and y values"""
        return x + ((ROWS - y) * COLS)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """

        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.
        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """

        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """

        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """

        pass


    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """

        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """

        pass

class Tile():
    def __init__(self, letter: str, value: int, is_empty: bool = False):
        self.sprite = arcade.Sprite(BASE_TILE)
        self.textSprite = arcade.create_text_sprite(letter, arcade.color.BLACK, font_size=24)
        self.sprite.size = (TILE_SIZE, TILE_SIZE)

        if not is_empty:
            self.letter = letter
            self.value = value
            self.sprite.color = arcade.color.TAN
        else:
            self.sprite.color = arcade.color.DARK_BROWN
    
    def update():
        arcade.draw



    
def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    scrabble = ScrabbleUI()

    window.show_view(scrabble)

    arcade.run()


main()