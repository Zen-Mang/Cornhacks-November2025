# src/entities.py
import arcade
from src import constants as c

# Note: You must create these PNG files in assets/images/
IMG_PATH = "Assets/images/"

class PlayerMonkey(arcade.Sprite):
    """ The monkey that throws. This one DOES NOT have physics. """
    def __init__(self):
        super().__init__(f"{IMG_PATH}/characters/chimps/throwering_chimp/throwing_chimp.png", c.PLAYER_SCALE)
        self.position = c.PLAYER_START_POS

# --- FIX IS HERE ---
# All of these just need to inherit from arcade.Sprite
# The physics engine will read the .mass, .friction, etc.
# attributes automatically when you add them.

class Banana(arcade.Sprite):  # <-- JUST arcade.Sprite
    """ The banana projectile. This one HAS physics. """
    def __init__(self):
        super().__init__(f"{IMG_PATH}/bamboo_wall/bamboo_wall.png", c.BANANA_SCALE)
        # Set Pymunk properties
        self.damping = c.BANANA_DAMPING
        self.mass = c.BANANA_MASS


class EnemyMonkey(arcade.Sprite):  # <-- JUST arcade.Sprite
    """ The enemy monkey in the tower. """
    def __init__(self, position):
        super().__init__(f"{IMG_PATH}/characters/apes/big_head_ape/big_head_ape.png", c.ENEMY_SCALE)
        self.position = position
        self.mass = c.ENEMY_MASS
        self.friction = c.ENEMY_FRICTION


class WallBlock(arcade.Sprite):  # <-- JUST arcade.Sprite
    """ The physics-enabled blocks that make up the tower. """
    def __init__(self, position):
        super().__init__(f"{IMG_PATH}/wood_wall/wood_wall.png", c.WALL_SCALE)
        self.position = position
        self.mass = c.WALL_MASS
        self.friction = c.WALL_FRICTION