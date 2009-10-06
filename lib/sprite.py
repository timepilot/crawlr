import pygame
from pygame.locals import *
from data import *
from constants import *
from terrain import TERRAIN_ALL

class BasicSprite(pygame.sprite.DirtySprite):
    """The base sprite from which all other sprites derive."""

    def __init__(self, window, map, width, height, direction, stop, start,
                 spritesheet, currentTerrain, currentRegion, imageList,
                 spriteCollideSize, spriteCollideOffset, animspeed,
                 spriteMovementSpeed):
        pygame.sprite.DirtySprite.__init__(self)
        self.SPRITE_COLLIDE_SIZE = spriteCollideSize
        self.SPRITE_COLLIDE_OFFSET = spriteCollideOffset
        self.SPRITE_MOVE_SPEED = spriteMovementSpeed
        self.window = window
        self.map = map
        self.width = width
        self.height = height
        self.direction = direction
        self.stop = stop
        self.start = start
        self.sprite = LoadSprite(spritesheet)
        self.current_terrain = currentTerrain
        self.current_region = currentRegion
        self.north = self.sprite.images(imageList['north'], -1)
        self.south = self.sprite.images(imageList['south'], -1)
        self.east = self.sprite.images(imageList['east'], -1)
        self.west = self.sprite.images(imageList['west'], -1)
        self.walking = {
            'up': self.north,
            'down': self.south,
            'right': self.east,
            'left': self.west}
        self.animcounter = 0
        self.animspeed = animspeed
        self.collide = {}
        self.current_space = 0
        self.frame = 0
        self.x = self.map.start_tile[0]*self.map.tile_size[0]
        self.y = self.map.start_tile[1]*self.map.tile_size[1]
        self.image = self.walking[self.map.start_direction][self.frame]
        self.rect = self.image.get_rect(left=self.x, top=self.y)
        self.collide_surface = pygame.Surface(spriteCollideSize)
        self.collide_rect = self.collide_surface.get_rect(
            left=self.rect.left + spriteCollideOffset[0],
            bottom=self.rect.bottom + spriteCollideOffset[1])

    def draw(self):
        """Cycle move animation frames and redraw at the new location."""

        self.animcounter = (self.animcounter + 1) % self.animspeed
        if self.animcounter == 0:
            self.frame = (self.frame + 1) % len(self.walking[self.direction])
        self.image = self.walking[self.direction][self.frame]
        self.collide_rect.left = self.rect.left - self.scroll_pos[0] + (
            self.SPRITE_COLLIDE_OFFSET[0])
        self.collide_rect.bottom = self.rect.bottom - self.scroll_pos[1] + (
            self.SPRITE_COLLIDE_OFFSET[1])

    def update(self):
        """Redraw the sprite if it moved."""

        self.movement = self.SPRITE_MOVE_SPEED
        if self.direction:
            if self.stop:
                self.stop_moving()
            else:
                self.move_check()
                self.move()
                self.draw()

    def stop_moving(self):
        """Stop moving sprite."""

        self.image = self.walking[self.direction][0]
        self.dirty = 1

    def move_check(self):
        pass

    def check_walls(self, key, rect):
        """Check if movement is blocked by a wall."""

        if pygame.Rect(rect).collidelistall(self.map.nowalk) != []:
            self.collide[key] = True
            if self.collide[self.direction]:
                self.stop = True
        else:
            self.collide[key] = False

    def check_terrain(self, rect):
        """Check the type of terrain the sprite moved to."""

        for type in TERRAIN_ALL:
            if type in self.map.types:
                if pygame.Rect(rect).collidelistall(
                    self.map.types[type]) != []:
                    self.current_terrain = type

    def check_region(self, rect):
        """Check the region the sprite moved to."""

        for region in self.map.region_numbers:
            if pygame.Rect(rect).collidelistall(
                self.map.regions[region]) != []:
                self.current_region = region


class PlayerSprite(BasicSprite):
    """The sprite for the character the player controls."""

    def __init__(self, window, map):
        width = PLAYER_WIDTH
        height = PLAYER_HEIGHT
        start_location = [ -(map.start_tile[0] * map.tile_size[0]),
                -(map.start_tile[0] * map.tile_size[1]) ]
        image_file = 'party'
        images = {
            'north': [
                (32, 144, width, height),
                (0, 144, width, height),
                (32, 144, width, height),
                (64, 144, width, height) ],
            'south': [
                (32, 0, width, height),
                (0, 0, width, height),
                (32, 0, width, height),
                (64, 0, width, height) ],
            'east': [
                (32, 96, width, height),
                (0, 96, width, height),
                (32, 96, width, height),
                (64, 96, width, height) ],
            'west': [
                (32, 48, width, height),
                (0, 48, width, height),
                (32, 48, width, height),
                (64, 48, width, height) ] }
        self.move_keys = []
        self.scroll_pos = [0,0]
        BasicSprite.__init__(self, window, map, width, height,
                None, True, start_location, image_file, "", "",
                images, PLAYER_COLLIDE_SIZE, PLAYER_COLLIDE_OFFSET,
                PLAYER_WALK_ANIMATION_SPEED, PLAYER_WALK_SPEED)


