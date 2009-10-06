from constants import *
from dice import Die
from sprite import PlayerSprite

class Player(PlayerSprite):
    """The main player character."""

    def __init__(self, window, map):
        PlayerSprite.__init__(self, window, map)
        name = "Player Name"

    def move(self):
        """Move the player."""

        self.dirty = 1
        direction = self.direction
        map_rect = self.map.mapLayer['terrain'].rect
        if not self.collide[direction]:
            if direction == "up":
                if self.rect.centery < SCROLL_TOP and self.scroll_pos[1] < 0:
                    self.scroll_pos[1] += self.movement
                    self.map.move_map([0, self.movement])
                else: self.rect.move_ip(0, -self.movement)
            elif direction == "down":
                if self.rect.centery > SCROLL_BOTTOM and (map_rect.height +
                        self.scroll_pos[1] > CAMERA_SIZE[1]):
                    self.scroll_pos[1] -= self.movement
                    self.map.move_map([0, -self.movement])
                else: self.rect.move_ip(0, self.movement)
            elif direction == "left":
                if self.rect.centerx < SCROLL_LEFT and self.scroll_pos[0] < 0:
                    self.scroll_pos[0] += self.movement
                    self.map.move_map([self.movement, 0])
                else: self.rect.move_ip(-self.movement, 0)
            elif direction == "right":
                if self.rect.centerx > SCROLL_RIGHT and (map_rect.width +
                        self.scroll_pos[0] > CAMERA_SIZE[0]):
                    self.scroll_pos[0] -= self.movement
                    self.map.move_map([-self.movement, 0])
                else: self.rect.move_ip(self.movement, 0)

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
        self.check_encounter()

    def check_encounter(self):
        """Check for a random encounter."""

        spaces = CHECK_SPACES_NORMAL
        if self.rect.collidelistall(self.map.danger) != []:
            spaces = CHECK_SPACES_DANGER
        self.current_space += 1
        if self.current_space == spaces + self.width:
            if Die(6).roll() == 6:
                pass
            self.current_space = 0

