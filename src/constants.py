# src/constants.py
import arcade

# --- Screen ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Banana Barrage"

# --- Physics (Tune these for fun) ---
GRAVITY = (0, -1000)
DEFAULT_DAMPING = 1.0
BANANA_DAMPING = 0.6
BANANA_MASS = 0.5
BANANA_FRICTION = 0.6

WALL_MASS = 1.0
WALL_FRICTION = 0.7
ENEMY_MASS = 0.8
ENEMY_FRICTION = 0.9

# --- Player ---
PLAYER_START_POS = (150, 200)
BANANA_START_POS = (PLAYER_START_POS[0] + 20, PLAYER_START_POS[1])
THROW_FORCE_MULTIPLIER = 4.0 # How powerful the throw is

# --- Sprite Scaling ---
PLAYER_SCALE = 1.0
BANANA_SCALE = 1.0
WALL_SCALE = 1.0
ENEMY_SCALE = 1.0

# --- Colors ---
BACKGROUND_COLOR = arcade.color.ALMOND