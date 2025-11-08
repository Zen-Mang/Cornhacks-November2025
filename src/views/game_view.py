# src/views/game_view.py
import arcade
from src import constants as c
from src.entities import PlayerMonkey, Banana, EnemyMonkey, WallBlock


class GameView(arcade.View):
    """
    Main game view
    """

    def __init__(self):
        super().__init__()
        arcade.set_background_color(c.BACKGROUND_COLOR)

        # --- Sprite Lists ---
        self.player_list = arcade.SpriteList()
        self.banana_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # --- Physics Engine ---
        self.physics_engine = None

        # --- Player Throwing Logic ---
        self.throw_start_pos = None
        self.throw_end_pos = None

    def setup(self):
        """ Set up the game. Call this to restart the level. """

        # 1. --- Initialize Physics Engine ---
        self.physics_engine = arcade.PymunkPhysicsEngine(
            damping=c.DEFAULT_DAMPING,
            gravity=c.GRAVITY
        )

        # 2. --- Create the Player ---
        self.player = PlayerMonkey()
        self.player_list.append(self.player)

        # 3. --- Create the Ground ---
        ground = arcade.SpriteSolidColor(2000, 20, arcade.color.BURLYWOOD)
        ground.position = (c.SCREEN_WIDTH / 2, 10)
        self.physics_engine.add_sprite(
            ground,
            friction=1.0,
            body_type=arcade.PymunkPhysicsEngine.STATIC
        )

        # 4. --- Build the Tower (Programmatically) ---
        # This is the "MVP" way. A flex goal is to load from Tiled.
        tower_x = c.SCREEN_WIDTH - 200

        # Base
        self.add_wall((tower_x - 50, 60))
        self.add_wall((tower_x, 60))
        self.add_wall((tower_x + 50, 60))

        # Enemy 1
        self.add_enemy((tower_x, 100))

        # Second floor
        self.add_wall((tower_x - 25, 140))
        self.add_wall((tower_x + 25, 140))

        # Enemy 2
        self.add_enemy((tower_x, 180))

        # 5. --- Add Sprite Lists to Physics Engine ---
        # This tells the engine to manage physics for all sprites in these lists.
        self.physics_engine.add_sprite_list(self.enemy_list, mass=c.ENEMY_MASS, friction=c.ENEMY_FRICTION)
        self.physics_engine.add_sprite_list(self.wall_list, mass=c.WALL_MASS, friction=c.WALL_FRICTION)
        self.physics_engine.add_sprite_list(self.banana_list, mass=c.BANANA_MASS, friction=c.BANANA_FRICTION)

    # --- Helper methods for setup ---
    def add_wall(self, position):
        wall = WallBlock(position)
        self.wall_list.append(wall)

    def add_enemy(self, position):
        enemy = EnemyMonkey(position)
        self.enemy_list.append(enemy)

    # --- Game Loop Methods ---
    def on_draw(self):
        """ Render the screen. """
        self.clear()

        # Draw all the sprite lists
        self.wall_list.draw()
        self.enemy_list.draw()
        self.banana_list.draw()
        self.player_list.draw()

        # Draw the "slingshot" line
        if self.throw_start_pos and self.throw_end_pos:
            arcade.draw_line(
                self.throw_start_pos[0], self.throw_start_pos[1],
                self.throw_end_pos[0], self.throw_end_pos[1],
                arcade.color.BROWN, 4
            )

    def on_update(self, delta_time):
        """ Run the physics simulation """
        self.physics_engine.step(delta_time)

    # --- Mouse Control Methods ---
    def on_mouse_press(self, x, y, button, modifiers):
        """ Store the start position of the "throw" """
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.throw_start_pos = (x, y)
            self.throw_end_pos = (x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """ Update the end position of the "throw" """
        if buttons & arcade.MOUSE_BUTTON_LEFT:
            self.throw_end_pos = (x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        """ Launch the banana! """
        if button == arcade.MOUSE_BUTTON_LEFT and self.throw_start_pos:
            start_x, start_y = self.throw_start_pos
            end_x, end_y = x, y

            # Calculate the force
            # The force is the *reverse* of the drag vector
            force_x = (start_x - end_x) * c.THROW_FORCE_MULTIPLIER
            force_y = (start_y - end_y) * c.THROW_FORCE_MULTIPLIER
            force = (force_x, force_y)

            # Create the banana
            banana = Banana()
            banana.position = c.BANANA_START_POS
            self.banana_list.append(banana)
            self.physics_engine.add_sprite(banana, mass=c.BANANA_MASS, friction=c.BANANA_FRICTION)

            # Apply the force
            self.physics_engine.apply_impulse(banana, force)

            # Reset the throw line
            self.throw_start_pos = None
            self.throw_end_pos = None