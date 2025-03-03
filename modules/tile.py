import arcade
from .config import TILE_SIZE

class Tile():
    """ 
    Class representing a tile

    Attributes:
        letter (str): The letter of the tile
        value (int): The score value of the tile
        image_path (str): The file path to the png of the graphic for the tile
    """
    def __init__(self, letter: str = '', value: int = 0, image_path="./assets/images/blank.png"):
        """ Initializes a tile object """
        self.letter = letter
        self.value = value
        self.image_path = image_path
        
        # Create a sprite for rendering tile graphics
        self.sprite = arcade.Sprite(image_path)
        self.sprite.size = (TILE_SIZE, TILE_SIZE)

# Dictionary to define and store all tiles
TILES = {
    "base": Tile(),
    "double_letter": Tile(image_path="./assets/images/double_letter.png"),
    "triple_letter": Tile(image_path="./assets/images/triple_letter.png"),
    "double_word": Tile(image_path="./assets/images/double_word.png"),
    "triple_word": Tile(image_path="./assets/images/triple_word.png"),
    "star": Tile(image_path="./assets/images/star.png"),
    "a": Tile('a', 1, "./assets/images/a.png"),
    "b": Tile('b', 3, "./assets/images/b.png"),
    "c": Tile('c', 3, "./assets/images/c.png"),
    "d": Tile('d', 2, "./assets/images/d.png"),
    "e": Tile('e', 1, "./assets/images/e.png"),
    "f": Tile('f', 4, "./assets/images/f.png"),
    "g": Tile('g', 2, "./assets/images/g.png"),
    "h": Tile('h', 4, "./assets/images/h.png"),
    "i": Tile('i', 1, "./assets/images/i.png"),
    "j": Tile('j', 8, "./assets/images/j.png"),
    "k": Tile('k', 5, "./assets/images/k.png"),
    "l": Tile('l', 1, "./assets/images/l.png"),
    "m": Tile('m', 3, "./assets/images/m.png"),
    "n": Tile('n', 1, "./assets/images/n.png"),
    "o": Tile('o', 1, "./assets/images/o.png"),
    "p": Tile('p', 3, "./assets/images/p.png"),
    "q": Tile('q', 10, "./assets/images/q.png"),
    "r": Tile('r', 1, "./assets/images/r.png"),
    "s": Tile('s', 1, "./assets/images/s.png"),
    "t": Tile('t', 1, "./assets/images/t.png"),
    "u": Tile('u', 1, "./assets/images/u.png"),
    "v": Tile('v', 4, "./assets/images/v.png"),
    "w": Tile('w', 4, "./assets/images/w.png"),
    "x": Tile('x', 8, "./assets/images/x.png"),
    "y": Tile('y', 4, "./assets/images/y.png"),
    "z": Tile('z', 10, "./assets/images/z.png"),
    "blank": Tile('', 0, "./assets/images/clear.png"),
}
