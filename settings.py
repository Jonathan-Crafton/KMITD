import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHTBLUE = (50,50,255)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# game settings
WIDTH = 528  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 384  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Keep Me In The Dark"
BGCOLOR = BROWN

FONT_NAME = 'arial'

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE


# Player settings
PLAYER_SPEED = 125
PLAYER_ROT_SPEED = 200
PLAYER_IMG = 'Player.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 40, 40)
BARREL_OFFSET = vec(30, 10)


# Mob settings
MOB_IMG = 'Shadow_3.png'
MOB_SPEEDS = [150, 100, 75, 125]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50

#SFX
WALKING_SFX = 'hard-footstep4.wav'
MENU_MUSIC = 'FullOfMemories.ogg'

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Items
ITEM_IMAGES = {'key': 'yellowKey.png'}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.4
