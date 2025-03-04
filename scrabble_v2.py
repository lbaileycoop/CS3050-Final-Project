from typing import Tuple
import arcade
from random import shuffle

# Dynamically adjust graphics according to user's display size
WINDOW_WIDTH = 750
WINDOW_HEIGHT = 750
WINDOW_TITLE = "Scrabble"
BOARD_SIZE = min(WINDOW_WIDTH, WINDOW_HEIGHT) * 0.6
ROWS = 15
COLS = 15
TILE_SIZE = int(BOARD_SIZE / 15)
TILE_GAP = TILE_SIZE * 0.1
DOCK_SIZE_X = BOARD_SIZE
DOCK_SIZE_Y = int(BOARD_SIZE / 4)
BORDER_X = (WINDOW_WIDTH - BOARD_SIZE) // 2
BORDER_Y = (WINDOW_HEIGHT - BOARD_SIZE) // 2

class Tile():
    """ 
    Class representing a tile

    Attributes:
        letter (str): The letter of the tile
        value (int): The score value of the tile
        image_path (str): The file path to the png of the graphic for the tile
    """
    def __init__(self, letter: str = '', value: int = 0, image_path="./assets/tiles/blank.png"):
        """ Initializes a tile object """
        self.letter = letter
        self.value = value
        self.image_path = image_path
        
        # Create a sprite for rendering tile graphics
        self.sprite = arcade.Sprite(image_path)
        self.sprite.size = (TILE_SIZE, TILE_SIZE)

    def set_letter(self, new_letter, value, new_letter_image: str):
        """ Sets a new letter and image for a blank tile """
        if self.letter == '':
            self.letter = new_letter
            self.value = value
            self.image_path = new_letter_image
            self.sprite.texture = arcade.load_texture(new_letter_image)

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


class Drawbag():
    """
    Class representing the draw bag

    Attributes:
        drawbag (lst): A list containing the tiles in the draw bag
    """
    def __init__(self):
        """ Initializes a draw bag object """
        self.drawbag = []
        self.initialize_drawbag()
    
    def add_tile(self, tile: Tile, quantity: int):
        """ Function to add a tile to the draw bag """
        for _ in range(quantity):
            self.drawbag.append(tile)

    def initialize_drawbag(self):
        """ Function to initialize the draw bag with the proper letter distribution """
        self.add_tile(TILES["a"], 9)
        self.add_tile(TILES["b"], 2)
        self.add_tile(TILES["c"], 2)
        self.add_tile(TILES["d"], 4)
        self.add_tile(TILES["e"], 12)
        self.add_tile(TILES["f"], 2)
        self.add_tile(TILES["g"], 3)
        self.add_tile(TILES["h"], 2)
        self.add_tile(TILES["i"], 9)
        self.add_tile(TILES["j"], 1)
        self.add_tile(TILES["k"], 1)
        self.add_tile(TILES["l"], 4)
        self.add_tile(TILES["m"], 2)
        self.add_tile(TILES["n"], 6)
        self.add_tile(TILES["o"], 8)
        self.add_tile(TILES["p"], 2)
        self.add_tile(TILES["q"], 1)
        self.add_tile(TILES["r"], 6)
        self.add_tile(TILES["s"], 4)
        self.add_tile(TILES["t"], 6)
        self.add_tile(TILES["u"], 4)
        self.add_tile(TILES["v"], 2)
        self.add_tile(TILES["w"], 2)
        self.add_tile(TILES["x"], 1)
        self.add_tile(TILES["y"], 2)
        self.add_tile(TILES["z"], 1)
        self.add_tile(TILES["blank"], 2)
        shuffle(self.drawbag)

    def draw_tile(self):
        """ Function to simulate drawing a tile from the draw bag """
        return self.drawbag.pop()
    
    def remaining_tiles(self):
        """ Function to get the amount of tiles remaining in the draw bag """
        return len(self.drawbag)
    
class Rack():
    """
    Class representing the rack of a player

    Attributes:
        rack(lst): A list containing the tiles a player currenlty has
    """
    def __init__(self, drawbag: Drawbag):
        """ Initializes a rack object for the start of the game """
        self.rack = []
        self.initialize_rack(drawbag)

    def add_tile(self, tile: Tile):
        """ Fucntion to add a tile to the current rack """
        self.rack.append(tile)
    
    def get_rack(self):
        """ Getter function for the rack list """
        return self.rack
    
    def remove_tile(self, tile: Tile):
        """ Removes a specified tile from the rack """
        self.rack.remove(tile)
    
    def initialize_rack(self, drawbag: Drawbag):
        """ Initializes a rack for the beginning of the game with 7 tiles from the draw bag """
        for _ in range(7):
            self.rack.append(drawbag.draw_tile())
    
    def len_rack(self):
        """ Function to get the amount of tiles in the current rack """
        return len(self.rack)
    
class Player():
    """
    Class representing a player

    Attributes:
        name (str): The player's name
        rack (Rack): The player's rack of tiles
        score (int): The player's current score
    """
    def __init__(self, name: str, drawbag: Drawbag):
        """ Initializes a player object """
        self.name = name
        self.rack = Rack(drawbag)
        self.score = 0

    def get_rack(self):
        """ Getter function for the player's current rack """
        return self.rack.get_rack()
    
    def get_score(self):
        """ Getter function for the player's current sore """
        return self.score
    
    def add_score(self, score: int):
        """ Function to increment the player's score """
        self.score += score

class Board():
    """
    Class representing the Scrabble board

    Attributes:
        board (lst) : 2D list representing the board's current state
    """
    def __init__(self):
        """ Initialize a board object """

        # 2D list to store the current board state
        self.board = [
            [TILES["triple_word"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_word"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["triple_word"]],
            [TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"]],
            [TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"]],
            [TILES["double_letter"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["double_letter"]],
            [TILES["base"], TILES["base"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["base"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["base"], TILES["base"]],
            [TILES["base"], TILES["triple_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_letter"], TILES["base"]],
            [TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"]],
            [TILES["triple_word"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["star"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["triple_word"]],
            [TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"]],
            [TILES["base"], TILES["triple_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_letter"], TILES["base"]],
            [TILES["base"], TILES["base"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["base"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["base"], TILES["base"]],
            [TILES["double_letter"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["double_letter"]],
            [TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"], TILES["base"]],
            [TILES["base"], TILES["double_word"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["double_word"], TILES["base"]],
            [TILES["triple_word"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["base"], TILES["triple_word"], TILES["base"], TILES["base"], TILES["base"], TILES["double_letter"], TILES["base"], TILES["base"], TILES["triple_word"]],
        ]
    
    def get_board(self):
        """ Getter function for the current board """
        return self.board

    def update_tile(self, x: int, y: int, tile: Tile):
        """ Function to update a tile in the board """
        self.board[y][x] = tile
    

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

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # Call draw() on all your sprite lists below
        self.board.draw()
        self.rack.draw()

    def to_coords(self, index: int) -> Tuple[int, int]:
        """Returns the x and y values of a tile based on the 1-d index"""
        return (index % COLS, (index // COLS))

    def from_coords(self, x: int, y: int) -> Tuple[int, int]:
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

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        if self.held_tile:
            self.held_tile.center_x = x
            self.held_tile.center_y = y

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        for i, tile in enumerate(self.rack_tiles):
            if tile.collides_with_point((x, y)):
                self.held_tile = tile
                self.held_tile_index = i
                break
                
    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        if self.held_tile:
            placed = False
            
            # If a tile is dropped over a space on the board, update the board position to that tlie
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

            if not placed:
                rack_index = None
                for i, rack_tile in enumerate(self.rack_tiles):
                    if rack_tile.collides_with_point((x, y)):
                        rack_index = i
                        

                # Swap tiles in player's rack (not necessarily correct)
                    if rack_index is not None and rack_index != self.held_tile_index:
                        self.player.rack.rack[self.held_tile_index], self.player.rack.rack[rack_index] = self.player.rack.rack[rack_index], self.player.rack.rack[self.held_tile_index]
                        self.original_rack_positions[self.held_tile_index], self.original_rack_positions[rack_index] = self.original_rack_positions[rack_index], self.original_rack_positions[self.held_tile_index]

                        self.rack_tiles[self.held_tile_index].center_x = self.original_rack_positions[self.held_tile_index][0]
                        self.rack_tiles[self.held_tile_index].center_y = self.original_rack_positions[self.held_tile_index][1]
                        self.rack_tiles[rack_index].center_x = self.original_rack_positions[rack_index][0]
                        self.rack_tiles[rack_index].center_y = self.original_rack_positions[rack_index][1]

                        self.rack_tiles[self.held_tile_index], self.rack_tiles[rack_index] = self.rack_tiles[rack_index], self.rack_tiles[self.held_tile_index]

                        self.logic_board.update_tile(self.held_tile_index, rack_index, self.player.rack.rack[self.held_tile_index])
                        self.logic_board.update_tile(rack_index, self.held_tile_index, self.player.rack.rack[rack_index])

            # If the tile is not dragged to a valid spot on the board, reset it back to rack
            if not placed and self.held_tile_index is not None:
                original_x, original_y = self.original_rack_positions[self.held_tile_index]
                self.held_tile.center_x = original_x
                self.held_tile.center_y = original_y

            
            self.held_tile = None
            self.held_tile_index = None


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    scrabble = ScrabbleUI()

    window.show_view(scrabble)

    arcade.run()

if __name__ == '__main__':
    main()