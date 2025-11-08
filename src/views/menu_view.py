# src/views/menu_view.py
import arcade
from src import constants as c
from src.views.game_view import GameView

class MenuView(arcade.View):
    """
    View for the main menu.
    """
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE_SMOKE)

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Banana Barrage",
            c.SCREEN_WIDTH / 2,
            c.SCREEN_HEIGHT / 2 + 100,
            arcade.color.BROWN,
            font_size=60,
            anchor_x="center",
        )
        arcade.draw_text(
            "Click to Start",
            c.SCREEN_WIDTH / 2,
            c.SCREEN_HEIGHT / 2,
            arcade.color.GRAY,
            font_size=30,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ Start the game """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)