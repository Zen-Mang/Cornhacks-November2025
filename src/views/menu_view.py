# src/views/menu_view.py
import arcade
from src import constants as c
from src.views.level_select_view import LevelSelectView


class MenuView(arcade.View):
    """
    View for the main menu.
    """

    def __init__(self):
        super().__init__()
        self.title_text = None
        self.start_text = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE_SMOKE)

        # Create text objects
        self.title_text = arcade.Text(
            "Banana Barrage",
            c.SCREEN_WIDTH / 2,
            c.SCREEN_HEIGHT / 2 + 100,
            arcade.color.BROWN,
            font_size=60,
            anchor_x="center",
            bold=True
        )

        self.start_text = arcade.Text(
            "Click to Start",
            c.SCREEN_WIDTH / 2,
            c.SCREEN_HEIGHT / 2,
            arcade.color.GRAY,
            font_size=30,
            anchor_x="center"
        )

    def on_draw(self):
        self.clear()
        self.title_text.draw()
        self.start_text.draw()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ Go to level select """
        level_select = LevelSelectView()
        self.window.show_view(level_select)