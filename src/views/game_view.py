# src/views/game_view.py
import arcade
from src import constants as c
from src.entities import PlayerMonkey, Banana, EnemyMonkey, BambooBlock, WoodBlock
from src.progress import progress


class GameView(arcade.View):
    """
    Main game view
    """

    def __init__(self, level_number=None):
        super().__init__()
        arcade.set_background_color(c.BACKGROUND_COLOR)

        # --- Sprite Lists ---
        self.player_list = arcade.SpriteList()
        self.banana_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bamboo_list = arcade.SpriteList()
        self.wood_list = arcade.SpriteList()

        # --- Physics Engine ---
        self.physics_engine = None

        # --- Player Throwing Logic ---
        self.throw_start_pos = None
        self.throw_end_pos = None

        # --- Tilemap ---
        self.tile_map = None

        # --- Level tracking ---
        self.level_number = level_number
        self.level_complete = False
        self.level_complete_timer = 0

        # --- UI Text ---
        self.level_text = None

    def setup(self, map_file=None):
        """
        Set up the game. Call this to restart the level.

        Args:
            map_file: Optional path to a Tiled .tmx file
        """

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

        # 4. --- Build the Level ---
        if map_file:
            self.load_tilemap(map_file)
        else:
            self.build_default_level()

        # 5. --- Add Sprite Lists to Physics Engine ---
        self.physics_engine.add_sprite_list(
            self.enemy_list,
            mass=c.ENEMY_MASS,
            friction=c.ENEMY_FRICTION
        )
        self.physics_engine.add_sprite_list(
            self.bamboo_list,
            mass=c.BAMBOO_MASS,
            friction=c.BAMBOO_FRICTION
        )
        self.physics_engine.add_sprite_list(
            self.wood_list,
            mass=c.WOOD_MASS,
            friction=c.WOOD_FRICTION
        )
        self.physics_engine.add_sprite_list(
            self.banana_list,
            mass=c.BANANA_MASS,
            friction=c.BANANA_FRICTION
        )

        # 6. --- Create UI Text ---
        if self.level_number:
            self.level_text = arcade.Text(
                f"Level {self.level_number}",
                10, c.SCREEN_HEIGHT - 30,
                arcade.color.BLACK,
                font_size=20,
                bold=True
            )

    def load_tilemap(self, map_file):
        """Load a Tiled map using arcade.load_tilemap."""
        # Load the tilemap
        self.tile_map = arcade.load_tilemap(map_file, scaling=1.0)

        # Get sprite lists from object layers based on their layer names
        # In Tiled, create Object Layers named: "Bamboo", "Wood", "Enemies"

        if "Bamboo" in self.tile_map.object_lists:
            for obj in self.tile_map.object_lists["Bamboo"]:
                bamboo = BambooBlock()
                bamboo.position = obj.position
                self.bamboo_list.append(bamboo)

        if "Wood" in self.tile_map.object_lists:
            for obj in self.tile_map.object_lists["Wood"]:
                wood = WoodBlock()
                wood.position = obj.position
                self.wood_list.append(wood)

        if "Enemies" in self.tile_map.object_lists:
            for obj in self.tile_map.object_lists["Enemies"]:
                enemy = EnemyMonkey()
                enemy.position = obj.position
                self.enemy_list.append(enemy)

        print(f"Loaded: {len(self.bamboo_list)} bamboo, {len(self.wood_list)} wood, {len(self.enemy_list)} enemies")

    def build_default_level(self):
        """Build a default programmatic level."""
        tower_x = c.SCREEN_WIDTH - 200

        # Base - mix of bamboo and wood
        bamboo1 = BambooBlock((tower_x - 50, 60))
        self.bamboo_list.append(bamboo1)

        wood1 = WoodBlock((tower_x, 60))
        self.wood_list.append(wood1)

        bamboo2 = BambooBlock((tower_x + 50, 60))
        self.bamboo_list.append(bamboo2)

        # Enemy 1
        enemy1 = EnemyMonkey((tower_x, 100))
        self.enemy_list.append(enemy1)

        # Second floor
        wood2 = WoodBlock((tower_x - 25, 140))
        self.wood_list.append(wood2)

        wood3 = WoodBlock((tower_x + 25, 140))
        self.wood_list.append(wood3)

        # Enemy 2
        enemy2 = EnemyMonkey((tower_x, 180))
        self.enemy_list.append(enemy2)

    # --- Game Loop Methods ---
    def on_draw(self):
        """ Render the screen. """
        self.clear()

        # Draw all sprite lists
        self.bamboo_list.draw()
        self.wood_list.draw()
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

        # Draw level text
        if self.level_text:
            self.level_text.draw()

        # Draw level complete message
        if self.level_complete:
            arcade.draw_rectangle_filled(
                c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2,
                400, 200, arcade.color.BLACK + (200,)
            )
            arcade.draw_text(
                "LEVEL COMPLETE!",
                c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2 + 40,
                arcade.color.YELLOW,
                font_size=40,
                anchor_x="center",
                bold=True
            )
            arcade.draw_text(
                "Returning to level select...",
                c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2 - 20,
                arcade.color.WHITE,
                font_size=20,
                anchor_x="center"
            )

    def on_update(self, delta_time):
        """ Run physics and handle collisions """
        if not self.level_complete:
            self.physics_engine.step(delta_time)
            self.check_collisions()

            # Check if level is complete (all enemies defeated)
            if len(self.enemy_list) == 0 and self.level_number:
                self.complete_level()
        else:
            # Count down timer to return to level select
            self.level_complete_timer += delta_time
            if self.level_complete_timer > 2.0:  # Wait 2 seconds
                self.return_to_level_select()

    def complete_level(self):
        """Mark the level as complete."""
        self.level_complete = True
        self.level_complete_timer = 0
        progress.complete_level(self.level_number)
        print(f"Level {self.level_number} complete! Level {self.level_number + 1} unlocked!")

    def return_to_level_select(self):
        """Return to the level selection screen."""
        from src.views.level_select_view import LevelSelectView
        level_select = LevelSelectView()
        self.window.show_view(level_select)

    def check_collisions(self):
        """Handle collision logic."""

        # Check banana hitting bamboo - bamboo breaks and slows banana
        for banana in self.banana_list:
            bamboo_hit = arcade.check_for_collision_with_list(banana, self.bamboo_list)
            for bamboo in bamboo_hit:
                phys_obj = self.physics_engine.get_physics_object(banana)
                if phys_obj:
                    velocity = phys_obj.body.velocity
                    speed = (velocity.x ** 2 + velocity.y ** 2) ** 0.5

                    if speed > c.COLLISION_SPEED_THRESHOLD:
                        # Break the bamboo
                        bamboo.remove_from_sprite_lists()

                        # Slow down banana
                        phys_obj.body.velocity = velocity * 0.5

        # Check enemies hit by banana, wood, or falling
        for enemy in list(self.enemy_list):
            # Check banana collision
            banana_hit = arcade.check_for_collision_with_list(enemy, self.banana_list)

            # Check wood collision
            wood_hit = arcade.check_for_collision_with_list(enemy, self.wood_list)

            if banana_hit or wood_hit:
                # Enemy disappears
                enemy.remove_from_sprite_lists()

        # Wood can also break bamboo when falling
        for wood in self.wood_list:
            bamboo_hit = arcade.check_for_collision_with_list(wood, self.bamboo_list)
            for bamboo in bamboo_hit:
                phys_obj = self.physics_engine.get_physics_object(wood)
                if phys_obj:
                    velocity = phys_obj.body.velocity
                    speed = (velocity.x ** 2 + velocity.y ** 2) ** 0.5

                    if speed > c.COLLISION_SPEED_THRESHOLD:
                        # Break the bamboo
                        bamboo.remove_from_sprite_lists()

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

    def on_key_press(self, key, modifiers):
        """Handle key presses."""
        if key == arcade.key.ESCAPE and not self.level_complete:
            self.return_to_level_select()