
# src/entities.py
import arcade
from src import constants as c

IMG_PATH = "assets/images/"

class PlayerMonkey(arcade.Sprite):
    """ The monkey that throws. This one DOES NOT have physics. """
    def __init__(self):
        super().__init__(f"{IMG_PATH}throwing_chimp.png", c.PLAYER_SCALE)
        self.position = c.PLAYER_START_POS

class Banana(arcade.Sprite):
    """ The banana projectile. This one HAS physics. """
    def __init__(self):
        super().__init__(f"{IMG_PATH}banana_sprite.png", c.BANANA_SCALE)
        self.damping = c.BANANA_DAMPING
        self.mass = c.BANANA_MASS


class EnemyMonkey(arcade.Sprite):
    """ The enemy monkey - disappears when hit. """
    def __init__(self, position=None):
        super().__init__(f"{IMG_PATH}big_head_ape.png", c.ENEMY_SCALE)
        if position:
            self.position = position
        self.mass = c.ENEMY_MASS
        self.friction = c.ENEMY_FRICTION


class BambooBlock(arcade.Sprite):
    """ Bamboo block that breaks when hit and slows down the banana. """
    def __init__(self, position=None):
        super().__init__(f"{IMG_PATH}bamboo_wall_1.png", c.BAMBOO_SCALE)
        if position:
            self.position = position
        self.mass = c.BAMBOO_MASS
        self.friction = c.BAMBOO_FRICTION


class WoodBlock(arcade.Sprite):
    """ Wood block that doesn't break but falls when hit. """
    def __init__(self, position=None):
        super().__init__(f"{IMG_PATH}wood_wall_1.png", c.WOOD_SCALE)
        if position:
            self.position = position
        self.mass = c.WOOD_MASS
        self.friction = c.WOOD_FRICTION


# Legacy support
class WallBlock(WoodBlock):
    """ Alias for WoodBlock for backwards compatibility. """
    pass
