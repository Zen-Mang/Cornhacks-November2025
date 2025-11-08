# src/views/level_select_view.py
import arcade
import os
from src import constants as c
from src.views.game_view import GameView
from src.progress import progress


class LevelButton:
    """A button for selecting a level."""

    def __init__(self, level_number, x, y, width, height, unlocked):
        self.level_number = level_number
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.unlocked = unlocked
        self.hovered = False

    def is_point_inside(self, x, y):
        """Check if a point is inside the button."""
        return (self.x - self.width / 2 < x < self.x + self.width / 2 and
                self.y - self.height / 2 < y < self.y + self.height / 2)

    def draw(self):
        """Draw the button."""
        # Choose colors based on state
        if not self.unlocked:
            color = arcade.color.GRAY
            text_color = arcade.color.DARK_GRAY
        elif self.hovered:
            color = arcade.color.ORANGE
            text_color = arcade.color.WHITE
        else:
            color = arcade.color.BROWN
            text_color = arcade.color.WHITE

        # Draw button background
        arcade.draw_rectangle_filled(
            self.x, self.y, self.width, self.height, color
        )

        # Draw border
        arcade.draw_rectangle_outline(
            self.x, self.y, self.width, self.height,
            arcade.color.BLACK, 3
        )

        # Draw level number
        arcade.draw_text(
            f"Level {self.level_number}",
            self.x, self.y,
            text_color,
            font_size=20,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        # Draw lock icon if locked
        if not self.unlocked:
            arcade.draw_text(
                "🔒",
                self.x, self.y - 35,
                arcade.color.DARK_GRAY,
                font_size=16,
                anchor_x="center",
                anchor_y="center"
            )


class LevelSelectView(arcade.View):
    """View for selecting levels."""

    def __init__(self):
        super().__init__()
        self.buttons = []
        self.available_levels = []
        self.title_text = None
        self.back_text = None

    def on_show_view(self):
        """Set up the view when shown."""
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

        # Find available level files
        self.available_levels = self.find_level_files()

        # Create buttons
        self.create_buttons()

        # Create text objects
        self.title_text = arcade.Text(
            "Select Level",
            c.SCREEN_WIDTH / 2,
            c.SCREEN_HEIGHT - 80,
            arcade.color.BROWN,
            font_size=50,
            anchor_x="center",
            bold=True
        )

        self.back_text = arcade.Text(
            "Press ESC to go back",
            c.SCREEN_WIDTH / 2,
            40,
            arcade.color.GRAY,
            font_size=18,
            anchor_x="center"
        )

    def find_level_files(self):
        """Find all level files in assets/levels/"""
        levels_dir = "assets/levels"
        levels = []

        if not os.path.exists(levels_dir):
            print(f"Warning: {levels_dir} directory not found!")
            return levels

        # Look for level1.tmx, level2.tmx, etc.
        level_num = 1
        while True:
            level_file = os.path.join(levels_dir, f"level{level_num}.tmx")
            if os.path.exists(level_file):
                levels.append((level_num, level_file))
                level_num += 1
            else:
                break

        return levels

    def create_buttons(self):
        """Create level selection buttons."""
        self.buttons = []

        # Button dimensions
        button_width = 150
        button_height = 80
        buttons_per_row = 4
        padding = 20

        # Calculate starting position
        start_x = (c.SCREEN_WIDTH - (buttons_per_row * (button_width + padding))) / 2 + button_width / 2
        start_y = c.SCREEN_HEIGHT - 200

        for i, (level_num, _) in enumerate(self.available_levels):
            row = i // buttons_per_row
            col = i % buttons_per_row

            x = start_x + col * (button_width + padding)
            y = start_y - row * (button_height + padding)

            unlocked = progress.is_level_unlocked(level_num)

            button = LevelButton(level_num, x, y, button_width, button_height, unlocked)
            self.buttons.append(button)

    def on_draw(self):
        """Draw the level selection screen."""
        self.clear()

        # Draw title
        self.title_text.draw()

        # Draw all buttons
        for button in self.buttons:
            button.draw()

        # Draw back text
        self.back_text.draw()

        # Draw info message if no levels found
        if not self.available_levels:
            arcade.draw_text(
                "No levels found in assets/levels/",
                c.SCREEN_WIDTH / 2,
                c.SCREEN_HEIGHT / 2,
                arcade.color.RED,
                font_size=24,
                anchor_x="center"
            )
            arcade.draw_text(
                "Create level1.tmx, level2.tmx, etc. in that folder",
                c.SCREEN_WIDTH / 2,
                c.SCREEN_HEIGHT / 2 - 40,
                arcade.color.GRAY,
                font_size=16,
                anchor_x="center"
            )

    def on_mouse_motion(self, x, y, dx, dy):
        """Handle mouse motion for button hover effects."""
        for button in self.buttons:
            button.hovered = button.is_point_inside(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse press to select a level."""
        if button == arcade.MOUSE_BUTTON_LEFT:
            for btn in self.buttons:
                if btn.is_point_inside(x, y) and btn.unlocked:
                    self.start_level(btn.level_number)

    def start_level(self, level_number):
        """Start the selected level."""
        # Find the level file
        level_file = None
        for num, file in self.available_levels:
            if num == level_number:
                level_file = file
                break

        if level_file:
            game_view = GameView(level_number=level_number)
            game_view.setup(map_file=level_file)
            self.window.show_view(game_view)

    def on_key_press(self, key, modifiers):
        """Handle key presses."""
        if key == arcade.key.ESCAPE:
            from src.views.menu_view import MenuView
            menu_view = MenuView()
            self.window.show_view(menu_view)