import pygame
from pygame.locals import *
from data import *
from constants import *
from dice import Die
from terrain import TERRAIN_ALL

class BasicSprite(pygame.sprite.DirtySprite):
    """The base sprite from which all other sprites derive."""

    def __init__(self, scene, width, height, start_direction, direction,
                stopped, start_location, spritesheet, image_dict, collide_size,
                collide_offset, speed_animate, speed_walk):
        pygame.sprite.DirtySprite.__init__(self)
        self.scene = scene
        self.window = scene.window
        self.map = scene.map
        self.width = width
        self.height = height
        self.start_direction = start_direction
        self.direction = direction
        self.stopped = stopped
        self.sprite = LoadSprite(spritesheet)
        self.current_terrain = ""
        self.current_region = ""
        self.north = self.sprite.images(image_dict['north'], -1)
        self.south = self.sprite.images(image_dict['south'], -1)
        self.east = self.sprite.images(image_dict['east'], -1)
        self.west = self.sprite.images(image_dict['west'], -1)
        self.walking = {
            'up': self.north,
            'down': self.south,
            'right': self.east,
            'left': self.west }
        self.speed_walk = speed_walk
        self.speed_animate = speed_animate
        self.animate_counter = 0
        self.current_space = 0
        self.frame = 0
        self.x = start_location[0]
        self.y = start_location[1]
        self.image = self.walking[self.start_direction][self.frame]
        self.rect = self.image.get_rect(left=self.x, top=self.y)
        self.collide = {}
        self.collide_size = collide_size
        self.collide_offset = collide_offset
        self.collide_surface = pygame.Surface(collide_size)
        self.collide_rect = self.collide_surface.get_rect(
            left=self.rect.left + collide_offset[0],
            bottom=self.rect.bottom + collide_offset[1])

    def draw(self):
        """Cycle move animation frames and redraw at the new location."""

        direction = self.walking[self.direction]
        self.animate_counter = (self.animate_counter + 1) % self.speed_animate
        if self.animate_counter == 0:
            self.frame = (self.frame + 1) % len(direction)
        self.image = direction[self.frame]
        self.collide_rect.left = self.rect.left - self.scroll_pos[0] + (
            self.collide_offset[0])
        self.collide_rect.bottom = self.rect.bottom - self.scroll_pos[1] + (
            self.collide_offset[1])

    def update(self):
        """Redraw the sprite if it moved."""

        self.movement = self.speed_walk
        if self.direction:
            if self.stop:
                self.image = self.walking[self.direction][0]
                self.dirty = 1
            else:
                self.move_check()
                self.move()
                self.draw()

    def move_check(self):
        """Check for walls, terrain, region, and random encounters."""

        directions = {
                'up': self.collide_rect.move(0, -self.movement),
                'down': self.collide_rect.move(0, self.movement),
                'left': self.collide_rect.move(-self.movement, 0),
                'right': self.collide_rect.move(self.movement, 0) }
        for key, rect in directions.iteritems():
            self.check_walls(key, rect)
            self.check_terrain(rect)
            self.check_region(rect)

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

    def __init__(self, scene):
        width = PLAYER_WIDTH
        height = PLAYER_HEIGHT
        start_location = [
            scene.map.start_tile[0] * scene.map.tile_size[0],
            scene.map.start_tile[1] * scene.map.tile_size[1] ]
        start_direction = scene.map.start_direction
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
        BasicSprite.__init__(self, scene, width, height,
                start_direction, None, True, start_location, image_file,
                images, PLAYER_COLLIDE_SIZE, PLAYER_COLLIDE_OFFSET,
                PLAYER_WALK_ANIMATION_SPEED, PLAYER_WALK_SPEED)

    def move(self):
        """Move the player."""

        self.check_encounter()
        self.dirty = 1
        direction = self.direction
        map_rect = self.map.layers['terrain'].rect
        if not self.collide[direction]:
            if direction == "up":
                if self.rect.centery < SCROLL_TOP and self.scroll_pos[1] < 0:
                    self.scroll_pos[1] += self.movement
                    self.scene.map.move_map([0, self.movement])
                    self.scene.monster.rect.move_ip([0, self.movement])
                else: self.rect.move_ip(0, -self.movement)
            elif direction == "down":
                if self.rect.centery > SCROLL_BOTTOM and (map_rect.height +
                        self.scroll_pos[1] > CAMERA_SIZE[1]):
                    self.scroll_pos[1] -= self.movement
                    self.scene.map.move_map([0, -self.movement])
                    self.scene.monster.rect.move_ip([0, -self.movement])
                else: self.rect.move_ip(0, self.movement)
            elif direction == "left":
                if self.rect.centerx < SCROLL_LEFT and self.scroll_pos[0] < 0:
                    self.scroll_pos[0] += self.movement
                    self.scene.map.move_map([self.movement, 0])
                    self.scene.monster.rect.move_ip([self.movement, 0])
                else: self.rect.move_ip(-self.movement, 0)
            elif direction == "right":
                if self.rect.centerx > SCROLL_RIGHT and (map_rect.width +
                        self.scroll_pos[0] > CAMERA_SIZE[0]):
                    self.scroll_pos[0] -= self.movement
                    self.scene.map.move_map([-self.movement, 0])
                    self.scene.monster.rect.move_ip([-self.movement, 0])
                else: self.rect.move_ip(self.movement, 0)

    def check_encounter(self):
        """Check for a random encounter."""

        spaces = CHECK_SPACES_NORMAL
        if self.rect.collidelistall(self.map.danger) != []:
            spaces = CHECK_SPACES_DANGER
        self.current_space += 1
        if self.current_space == spaces * self.width:
            if Die(6).roll() == 6:
                print "TODO: random encounter"
            self.current_space = 0


class MonsterSprite(BasicSprite):

    def __init__(self, scene):
        width = 32
        height = 48
        start_location = [
            scene.map.start_tile[0]-1 * scene.map.tile_size[0],
            scene.map.start_tile[1]+12 * scene.map.tile_size[1] ]
        start_direction = scene.map.start_direction
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
        BasicSprite.__init__(self, scene, width, height,
                start_direction, None, True, start_location, image_file,
                images, PLAYER_COLLIDE_SIZE, PLAYER_COLLIDE_OFFSET,
                PLAYER_WALK_ANIMATION_SPEED, PLAYER_WALK_SPEED)
