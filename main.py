import arcade
from ui import StartScreen, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    start_screen = StartScreen()  # Start with the start screen
    window.show_view(start_screen)
    arcade.run()

if __name__ == '__main__':
    main()