# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (160, 160, 0)
GREY = (100, 100, 100)

COLOR_POWER_BAR = (100,50,138)
COLOR_POWER_BAR_EMPTY = (0,0,0,1)

BACKGROUND_COLOR = (255,255,255)

COLOR_MENU_1 = (255,212,0)
COLOR_MENU_2 = (0, 0, 0)
COLOR_MENU_FONTS = (0, 0, 0)

COLOR_MENU_SELECT_1 = (255, 102, 0)
COLOR_MENU_SELECT_2 = (255, 255, 255)
COLOR_MENU_FONTS_SELECT = (255,255,255)

#Main font
FONT_NAME = 'arial'

FPS = 60

#DIMENSION
# http://gamedevelopment.tutsplus.com/articles/quick-tip-what-is-the-best-screen-resolution-for-your-game--gamedev-14723
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_WIDTH = 32
TILE_HEIGHT = 32

# Development mode, DEV or OPT
DEV_MODE = 1
OPT_MODE = 0
MODE = DEV_MODE

# To get which mouse button is pressed.
MOUSE_LEFT = 1
MOUSE_RIGHT = 3

#Scenes self.nextScene commands, used to tell SceneHandler what next scene to run after this one ends
TITLE_SCREEN = 0
SHOP_SCREEN = 1
INSTRUCTION_SCREEN = 911
WIN_SCREEN = 3
GAME_OVER_SCREEN = 4
CREDIT_SCREEN = 5

PLATFORM_SCREEN = 42

# Sprite Layer
SPRITE_LAYER = 4
CAMERA_HUD_LAYER = 5

#Facing Sides
RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3

#Collisions
COLLISION_LAYER = 0
SOLID = 1 #Booléen de GID pour collision
SPIKE = 2
SPRING = 3
LADDER = 4
NONE = 5 #Pour identifier qu'il n'y a eu aucune collision

OBSTACLE = 100 #This is not a tile

#Player jump states
GROUNDED = 0
JUMP = 1
CLIMBING = 2 #When on a ladder

#Physics
GRAVITY = 1
FRICTION = 0.8

#Projectiles
GRENADE_SPEEDX = 2
GRENADE_SPEEDY = 2
BARRICADE_DISTANCE = 50
TARGET_DISTANCE = BARRICADE_DISTANCE

#ENEMY MODE
WALKING = 1
PREPARE_ATTACK = 2
IN_ATTACK = 3

POWER_CAP = 9
RATIO = 5

# Dimension tile base for icon
TILEDIMX = 32
TILEDIMY = 32

#GUI settings
DIALOG_TEXT_SIZE = 20
INPUT_BOX_FONT = "Arial"
INPUT_BOX_TEXT_SIZE = 20
MENU_FONT = "Arial"
MENU_FONT_COLOR = BLUE
COLOR_MENU_1 = WHITE
COLOR_MENU_2 = BLACK
COLOR_MENU_SELECT_1 = (150,150,150)
COLOR_MENU_SELECT_2 = BLUE
COLOR_MENU_FONT_SELECT = WHITE
HUD_FONT_COLOR = WHITE

# If you add a Tag for debugging, you MUST set it here at 0 for everyone
# You can turn your tag on in your own settings_local.py for personal use

TAG_BP = 0
TAG_MARIE = 0
TAG_PHIL = 0
TAG_ANIKA = 0

# Load settings_local.py if exist
try:
    from app.settings_local import *
except ImportError:
    pass