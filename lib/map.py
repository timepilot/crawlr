from random import choice
import pygame
from pygame.locals import *
from config import *
from constants import *
from data import load_map
from terrain import *
from dice import Die

class Map(object):
    """The game world."""

    def __init__(self, level):
        self.layers = []
        self.nowalk = []
        self.danger = []
        self.types = {}
        self.regions = {}
        self.mapPos = {}
        self.terrain = {
            PLAINS: TerrainPlains(),
            DIRT: TerrainDirt(),
            FOREST: TerrainForest(),
            WATER: TerrainWater() }
        self.mapLayer = {}
        self.mapConfig = load_map(level)
        self.create_map()

    def configure(self):
        """Reads and stores keys from the map config."""

        mapOptions = self.mapConfig['Options']
        self.start_tile = [
            int(mapOptions['start_tile'][0]),
            int(mapOptions['start_tile'][1]) ]
        self.tile_size = [
            int(mapOptions['tile_size'][0]),
            int(mapOptions['tile_size'][1]) ]
        self.num_tiles = [
            int(mapOptions['num_tiles'][0]),
            int(mapOptions['num_tiles'][1]) ]
        self.region_numbers = mapOptions['regions']
        self.start_direction = mapOptions['start_direction']

    def create_map(self):
        """Reads and creates the map from the config."""

        self.configure()
        self.create_layers()
        self.store_terrains()
        self.draw_map()

    def create_layers(self):
        """Create the map's layers."""

        temp_layer = []
        mapLayers = self.mapConfig['Layers']
        for layer in mapLayers:
            for line in mapLayers[layer]:
                temp_layer.append(mapLayers[layer][line])
            self.layers.append(temp_layer)
            temp_layer = []
        self.mapLayer['terrain'] = MapLayer(self.tile_size[0],
            len(self.layers[0][0]), self.tile_size[1], len(self.layers[0]))
        self.mapLayer['foreground'] = MapLayer(self.tile_size[0],
            len(self.layers[0][0]), self.tile_size[1], len(self.layers[0]))

    def get_size(self):
        """Get the size of the map."""

        w = self.num_tiles[0] * self.tile_size[0]
        h = self.num_tiles[1] * self.tile_size[1]
        return (w, h)

    def store_terrains(self):
        """Sets each tile's position and terrain type."""

        row_num = 0
        tile_num = 0
        for row in self.layers[LAYER_TERRAIN]:
            for tile in row:
                offset = (tile_num * self.tile_size[0],
                    row_num * self.tile_size[1])
                self.set_terrain(tile, offset)
                tile_num+=1
            row_num+=1
            tile_num = 0

    def draw_map(self):
        """Draws the layers to the map."""

        for layer in range(0, len(self.layers)):
            row_num = 0
            tile_num = 0
            for row in self.layers[layer]:
                for tile in row:
                    offset = (tile_num * self.tile_size[0],
                        row_num * self.tile_size[1])
                    self.draw_tile(layer, tile, offset)
                    tile_num+=1
                row_num+=1
                tile_num = 0

    def draw_tile(self, layer, tile, offset):
        """Draws a tile to the correct layer."""

        terrain = self.mapPos[offset]
        blit = self.mapLayer['terrain'].image.blit

        if tile != ".":
            if layer == LAYER_DATA:
                if tile == "X":
                    self.set_nowalk(offset)
                elif tile.isdigit():
                    self.set_region(tile, offset)

            elif layer == LAYER_TERRAIN:
                blit(terrain[0].image, offset)
                self.set_edges(offset)
                self.draw_transitions(terrain, offset)
                terrain[0].draw_details(self.mapLayer['terrain'], offset)
                if not terrain[0].walkable:
                    self.set_nowalk(offset)

            elif layer == LAYER_OBJECTS:
                tiles = terrain[0].objects[tile]
                image = tiles[TILE_IMAGE]
                size = tiles[TILE_SIZE]
                pos = tiles[TILE_POS]
                slice = tiles[TILE_SLICE]
                walk = tiles[TILE_WALKABLE]
                w = image.get_width()
                h = image.get_height()
                offset = self.align_objects(w, h, offset)
                blit(image, offset)
                if not walk:
                    self.set_nowalk(offset, size, pos)
                self.set_above(w, h, image, offset, slice)

    def draw_transitions(self, terrain, offset):
        """Draws edges to transition cleanly with unlike terrain types."""

        order = terrain[0].order
        edges = terrain[0].edges
        corners = terrain[0].corners
        sides = ('n', 'e', 's', 'w')
        diags = ('ne', 'se', 'sw', 'nw')
        blit = self.mapLayer['terrain'].image.blit
        dict = terrain[1]

        if offset in self.mapPos:
            for depth in range(4):
                if depth > order:
                    for type in (FOREST, DIRT):

                        # Draw side transitions
                        for key in sides:
                            if type in edges and dict.get(key) == type:
                                blit(edges[type][0][key], offset)

                        # Draw curve transitions
                        for key in diags:
                            if dict.get(key[0]) == type and (
                                dict.get(key[1]) == type):
                                blit(edges[type][0][key[0]+key[1]], offset)
                            if type in corners and dict.get(key) == type:
                                blit(corners[type][0][key], offset)

                    if type in TERRAIN_UNWALKABLE:
                        self.set_nowalk(offset)

    def set_edges(self, offset):
        """Loops through all adjacent tiles and stores their terrain types."""

        rect = Rect((offset[0], offset[1],
            self.tile_size[0], self.tile_size[1]))
        edges = {
            'n':  rect.move(0,-32),
            'ne': rect.move(32,-32),
            'e':  rect.move(32,0),
            'se': rect.move(32,32),
            's':  rect.move(0,32),
            'sw': rect.move(-32,32),
            'w':  rect.move(-32,0),
            'nw': rect.move(-32,-32) }
        for edge in edges:
            current = (edges[edge][0], edges[edge][1])
            curX, curY = current
            maxX, maxY = self.get_size()
            if (0 <= curX <= maxX and 0 <= curY <= maxY and
                current in self.mapPos and offset in self.mapPos):
                self.mapPos[offset][1][edge] = self.mapPos[current][0].type

    def align_objects(self, w, h, offset):
        """Re-align bigger tiles to fit the rest."""

        object_offset = [0,0]
        offset = [offset[0], offset[1]]
        if not self.tile_size[0] == w:
            object_offset[0] = self.tile_size[0]-w/2
            offset[0] += object_offset[0]
        if not self.tile_size[1] == h:
            object_offset[1] = self.tile_size[1]-h
            offset[1] += object_offset[1]
        return offset

    def move_map(self, offset):
        """Scroll the map when when the player needs it to move."""

        self.mapLayer['terrain'].dirty = 1
        for layer in self.mapLayer:
            self.mapLayer[layer].rect.move_ip(offset)

    def set_nowalk(self, offset, size=[32,32], pos=[0,0]):
        """Sets the parts of the tile that are unwalkable."""

        rect = Rect(offset[0] + pos[0], offset[1] + pos[1], size[0], size[1])
        self.nowalk.append(rect)

    def set_above(self, width, height, tile, offset, section):
        """Draws the correct piece of the tile to the foreground."""

        if (width > self.tile_size[0]) or (height > self.tile_size[1]):
            self.mapLayer['foreground'].image.blit(tile, offset, section)

    def set_terrain(self, tile, offset, size=[32,32], pos=[0,0]):
        """Sets the terrain type of the tile."""

        # Make each terrain more natural by mixing in another similar type.
        if Die(10).roll() == 1:
            if tile == PLAINS:
                tile = DIRT
            elif tile == FOREST:
                tile = PLAINS

        # Store the final terrain type of the tile.
        if tile in self.terrain:
            tile_rect = Rect(offset[0] + pos[0], offset[1] + pos[1], size[0],
                size[1])
            self.terrain[tile].collide.append(tile_rect)
            self.types[tile] = self.terrain[tile].collide
            self.mapPos[offset] = [ self.terrain[tile], {} ]

    def set_region(self, tile, offset, size=[32,32], pos=[0,0]):
        """Sets the region number for the tile."""

        rect = Rect(offset[0] + pos[0], offset[1] + pos[1], size[0], size[1])
        if tile in self.regions:
            self.regions[tile].append(rect)
        else:
            self.regions[tile] = []


class MapLayer(pygame.sprite.DirtySprite):
    """Creates a map layer."""

    def __init__(self, w, numx, h, numy):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface((w * numx, h * numy), SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
