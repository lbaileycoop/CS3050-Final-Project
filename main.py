import arcade
from ui import ScrabbleUI, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    scrabble = ScrabbleUI()
    window.show_view(scrabble)
    arcade.run()

if __name__ == '__main__':
    main()