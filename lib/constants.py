import pygame
from pygame.locals import *
from config import *

# Display
CAMERA_SIZE = [ WINDOW_SIZE[0], WINDOW_SIZE[1] ]

# Events
BATTLE_EVENT = pygame.USEREVENT + 1
DIALOG_EVENT = pygame.USEREVENT + 2

# GUI
DIALOG_SIZE = (478, 192)
DIALOG_MAX_SIZE = [ DIALOG_SIZE[0] - 32, DIALOG_SIZE[1] - 32 ]
DIALOG_POSITION = WINDOW_SIZE[1] - 96
DIALOG_TILES = [ DIALOG_SIZE[0] / 16, DIALOG_SIZE[1] / 16 ]
DIALOG_TEXT_SIZE = 16
DIALOG_TEXT_COLOR = (224,224,224)
DIALOG_BUFFER_SIZE = (DIALOG_SIZE[0], 10000)
STATS_SIZE = (256, 64)
STATS_TILES = [ STATS_SIZE[0] / 16, STATS_SIZE[1] / 16 ]
STATS_SPACING = 72
STATS_TEXT_SIZE = 10
STATS_TEXT_FGCOLOR = (255,255,255)
STATS_TEXT_BGCOLOR = (0,0,0)

# Map
TILE_IMAGE = 0
TILE_WALKABLE = 1
TILE_SLICE = 2
TILE_SIZE = 3
TILE_POS = 4

# Layers:
LAYERS_NUM = 3
LAYER_DATA =    0
LAYER_TERRAIN = 1
LAYER_OBJECTS = 2

# Terrain
TERRAIN_GRASS = [ 'g', 'g2', 'g3' ]
TERRAIN_FOREST = [ 'f' ]
TERRAIN_ALL_WORLD = [TERRAIN_GRASS, TERRAIN_FOREST]
TERRAIN_TRANSITIONS = [
    TERRAIN_GRASS[1],
    TERRAIN_GRASS[2],
    TERRAIN_FOREST[0] ]
TERRAIN_UNWALKABLE = []
TERRAIN_RANDOMNESS = 5

# Characters
CHAR_WIDTH = 32
CHAR_HEIGHT = 48

# Player
PLAYER_SCROLL_TOP = CAMERA_SIZE[1]/3
PLAYER_SCROLL_BOTTOM = CAMERA_SIZE[1] - (CAMERA_SIZE[1]/3)
PLAYER_SCROLL_LEFT = CAMERA_SIZE[0]/3
PLAYER_SCROLL_RIGHT = CAMERA_SIZE[0] - (CAMERA_SIZE[0]/3)
PLAYER_MOVEMENT_NORMAL = 3
PLAYER_MOVEMENT_DANGER = 1
PLAYER_ENCOUNTER_ROLL = 3
PLAYER_WALK_SPEED = 2
PLAYER_WALK_ANIMATION_SPEED = 6
PLAYER_COLLIDE_SIZE = [ 11, 11 ]
PLAYER_COLLIDE_OFFSET = [ 11, -1 ]

# Monsters
MONSTERS_MAX_AMOUNT = 4
