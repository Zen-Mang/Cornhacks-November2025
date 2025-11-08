# main.py
import arcade
from src import constants as c
from src.views.menu_view import MenuView

def main():
    """ Main function """
    window = arcade.Window(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
