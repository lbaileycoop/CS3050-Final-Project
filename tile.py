import arcade

class Tile:
    """
    Class representing a tile

    Attributes:
        letter (str): The letter of the tile
        value (int): The score value of the tile
        image_path (str): The file path to the png of the graphic for the tile
    """
    def __init__(self, letter: str = '', value: int = 0, image_path: str = "./assets/tiles/blank.png"):
        """ Initializes a tile object """
        self.letter = letter
        self.value = value
        self.image_path = image_path

        # Create a sprite for rendering tile graphics
        self.sprite = arcade.Sprite(image_path)
        self.sprite.size = (TILE_SIZE, TILE_SIZE)

# Constants for window and board sizing (used across files)
WINDOW_WIDTH, WINDOW_HEIGHT = arcade.get_display_size()
BOARD_SIZE = min(WINDOW_WIDTH, WINDOW_HEIGHT) * 0.45
TILE_SIZE = int(BOARD_SIZE / 15)

# Dictionary to define and store all tiles
TILES = {
    "base": Tile(),
    "double_letter": Tile(image_path="./assets/tiles/double_letter.png"),
    "triple_letter": Tile(image_path="./assets/tiles/triple_letter.png"),
    "double_word": Tile(image_path="./assets/tiles/double_word.png"),
    "triple_word": Tile(image_path="./assets/tiles/triple_word.png"),
    "star": Tile(image_path="./assets/tiles/star.png"),
    "a": Tile('a', 1, "./assets/tiles/a.png"),
    "b": Tile('b', 3, "./assets/tiles/b.png"),
    "c": Tile('c', 3, "./assets/tiles/c.png"),
    "d": Tile('d', 2, "./assets/tiles/d.png"),
    "e": Tile('e', 1, "./assets/tiles/e.png"),
    "f": Tile('f', 4, "./assets/tiles/f.png"),
    "g": Tile('g', 2, "./assets/tiles/g.png"),
    "h": Tile('h', 4, "./assets/tiles/h.png"),
    "i": Tile('i', 1, "./assets/tiles/i.png"),
    "j": Tile('j', 8, "./assets/tiles/j.png"),
    "k": Tile('k', 5, "./assets/tiles/k.png"),
    "l": Tile('l', 1, "./assets/tiles/l.png"),
    "m": Tile('m', 3, "./assets/tiles/m.png"),
    "n": Tile('n', 1, "./assets/tiles/n.png"),
    "o": Tile('o', 1, "./assets/tiles/o.png"),
    "p": Tile('p', 3, "./assets/tiles/p.png"),
    "q": Tile('q', 10, "./assets/tiles/q.png"),
    "r": Tile('r', 1, "./assets/tiles/r.png"),
    "s": Tile('s', 1, "./assets/tiles/s.png"),
    "t": Tile('t', 1, "./assets/tiles/t.png"),
    "u": Tile('u', 1, "./assets/tiles/u.png"),
    "v": Tile('v', 4, "./assets/tiles/v.png"),
    "w": Tile('w', 4, "./assets/tiles/w.png"),
    "x": Tile('x', 8, "./assets/tiles/x.png"),
    "y": Tile('y', 4, "./assets/tiles/y.png"),
    "z": Tile('z', 10, "./assets/tiles/z.png"),
    "blank": Tile('', 0, "./assets/tiles/clear.png"),
}