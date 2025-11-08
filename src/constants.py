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

# --- Bamboo Block Properties ---
BAMBOO_MASS = 0.3  # Lighter, breaks easily
BAMBOO_FRICTION = 0.5
BAMBOO_SCALE = 1.0

# --- Wood Block Properties ---
WOOD_MASS = 1.0  # Heavier, doesn't break
WOOD_FRICTION = 0.7
WOOD_SCALE = 1.0

# --- Enemy Properties ---
ENEMY_MASS = 0.8
ENEMY_FRICTION = 0.9
ENEMY_SCALE = 1.0

# --- Legacy support ---
WALL_MASS = WOOD_MASS
WALL_FRICTION = WOOD_FRICTION
WALL_SCALE = WOOD_SCALE

# --- Player ---
PLAYER_START_POS = (150, 200)
BANANA_START_POS = (PLAYER_START_POS[0] + 20, PLAYER_START_POS[1])
THROW_FORCE_MULTIPLIER = 4.0

# --- Sprite Scaling ---
PLAYER_SCALE = 1.0
BANANA_SCALE = 1.0

# --- Colors ---
BACKGROUND_COLOR = arcade.color.ALMOND

# --- Collision Detection ---
COLLISION_SPEED_THRESHOLD = 100  # Minimum speed to trigger effects