# src/entities.py
import arcade
from src import constants as c

IMG_PATH = "assets/images/"

class PlayerMonkey(arcade.Sprite):
    """ The monkey that throws. This one DOES NOT have physics. """
    def __init__(self):
        super().__init__(f"{IMG_PATH}throwing_chimp.png", c.PLAYER_SCALE)
        self.position = c.PLAYER_START_POS

class Banana(arcade.Sprite):  # <-- JUST arcade.Sprite
    """ The banana projectile. This one HAS physics. """
    def __init__(self):
        super().__init__(f"{IMG_PATH}bamboo_wall.png", c.BANANA_SCALE)

        self.damping = c.BANANA_DAMPING
        self.mass = c.BANANA_MASS


class EnemyMonkey(arcade.Sprite):  # <-- JUST arcade.Sprite
    """ The enemy monkey in the tower. """
    def __init__(self, position):
        super().__init__(f"{IMG_PATH}big_head_ape.png", c.ENEMY_SCALE)
        self.position = position
        self.mass = c.ENEMY_MASS
        self.friction = c.ENEMY_FRICTION


class WallBlock(arcade.Sprite):
    """ The physics-enabled blocks that make up the tower. """
    def __init__(self, position):
        super().__init__(f"{IMG_PATH}wood_wall.png", c.WALL_SCALE)
        self.position = position
        self.mass = c.WALL_MASS
        self.friction = c.WALL_FRICTION