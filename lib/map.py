import pygame
from pygame.locals import *
from constants import *
from data import load_map
from terrain import *
from dice import Die

class Map(object):
    """The game world."""

    def __init__(self, level):
        self.nowalk = []
        self.danger = []
        self.types = {}
        self.regions = {}
        self.position = {}
        self.tile_dict = {}
        self.terrain = {
            TERRAIN_GRASS[0]:           TerrainGrass(0),
            TERRAIN_GRASS[1]:           TerrainGrass(1),
            TERRAIN_GRASS[2]:           TerrainGrass(2),
            TERRAIN_CAVE_FLOOR[0]:      TerrainCaveFloor(0),
            TERRAIN_CAVE_CEILING[0]:    TerrainCaveCeiling(0),
            TERRAIN_FOREST[0]:          TerrainForest(0) }
        self.layer_list = []
        self.layers = {}
        self.config = load_map(level)
        self.create_map()

    def configure(self):
        """Reads and stores keys from the map config."""

        options = self.config['Options']
        tile_set = options['tile_set']
        if tile_set == 'cave':
            self.terrain_list = TERRAIN_ALL_CAVE
        elif tile_set == 'world':
            self.terrain_list = TERRAIN_ALL_WORLD
        self.start_tile = [
            int(options['start_tile'][0]),
            int(options['start_tile'][1]) ]
        self.tile_size = [
            int(options['tile_size'][0]),
            int(options['tile_size'][1]) ]
        self.num_tiles = [
            int(options['num_tiles'][0]),
            int(options['num_tiles'][1]) ]
        self.region_numbers = options['regions']
        self.start_direction = options['start_direction']

    def create_map(self):
        """Reads and creates the map from the config."""

        self.configure()
        self.create_layers()
        self.store_terrains()
        self.draw_map()

    def create_layers(self):
        """Create the map's layers."""

        temp_layer = []
        layers = self.config['Layers']
        for layer in layers:
            for line in layers[layer]:
                temp_layer.append(layers[layer][line])
            self.layer_list.append(temp_layer)
            temp_layer = []
        self.layers['terrain'] = LayerSprite(self.tile_size[0],
            len(self.layer_list[0][0]), self.tile_size[1],
            len(self.layer_list[0]))
        self.layers['foreground'] = LayerSprite(self.tile_size[0],
            len(self.layer_list[0][0]), self.tile_size[1],
            len(self.layer_list[0]))

    def get_size(self):
        """Get the size of the map."""

        w = self.num_tiles[0] * self.tile_size[0]
        h = self.num_tiles[1] * self.tile_size[1]
        return (w, h)

    def store_terrains(self):
        """Sets each tile's position and terrain type."""

        row_num = 0
        tile_num = 0
        for row in self.layer_list[LAYER_TERRAIN]:
            for tile in row:
                offset = (tile_num * self.tile_size[0],
                    row_num * self.tile_size[1])
                self.tile_dict[offset] = tile
                self.set_terrain(offset)
                tile_num+=1
            row_num+=1
            tile_num = 0

    def set_terrain(self, offset):
        """Sets the terrain type of the tile."""

        tile = self.tile_dict[offset]
        rect = Rect(offset[0], offset[1],
            self.tile_size[0], self.tile_size[1])

        # Make each terrain more natural by mixing in another similar type.
        check = Die(TERRAIN_RANDOMNESS).roll()
        if check == 1:
            for terrain in self.terrain_list:
                if tile == terrain[0]:
                    choice = Die(len(terrain)).roll()-1
                    tile = terrain[choice]

        self.terrain[tile].collide.append(rect)
        self.types[tile] = self.terrain[tile].collide
        self.position[offset] = [ self.terrain[tile], {} ]

    def draw_map(self):
        """Draws the layers to the map."""

        for layer in range(0, len(self.layer_list)):
            row_num = 0
            tile_num = 0
            for row in self.layer_list[layer]:
                for tile in row:
                    offset = (tile_num * self.tile_size[0],
                        row_num * self.tile_size[1])
                    self.draw_tile(layer, tile, offset)
                    tile_num+=1
                row_num+=1
                tile_num = 0

    def draw_tile(self, layer, tile, offset):
        """Draws a tile to the correct layer."""

        terrain = self.position[offset]
        blit = self.layers['terrain'].image.blit

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
                terrain[0].draw_details(self.layers['terrain'], offset)
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
        blit = self.layers['terrain'].image.blit
        dict = terrain[1]

        if offset in self.position:
            for depth in range(3):
                if depth > order:
                    for type in TERRAIN_TRANSITIONS:

                        # Draw side transitions
                        for key in sides:
                            if type in edges and (dict.get(key) == type):
                                blit(edges[type][0][key], offset)

                        # Draw curve transitions
                        for key in diags:
                            if dict.get(key[0]) == type and (
                                dict.get(key[1]) == type):
                                blit(edges[type][0][key[0]+key[1]], offset)
                            if type in corners and (dict.get(key) == type):
                                blit(corners[type][0][key], offset)

                        if type in TERRAIN_UNWALKABLE:
                            self.set_nowalk(offset)

    def set_edges(self, offset):
        """Loops through all adjacent tiles and stores their terrain types."""

        rect = Rect((offset[0], offset[1],
            self.tile_size[0], self.tile_size[1]))
        w, h = self.tile_size[0], self.tile_size[1]
        edges = {
            'n':  rect.move(0,-h),
            'ne': rect.move(w,-h),
            'e':  rect.move(w,0),
            'se': rect.move(w,h),
            's':  rect.move(0,h),
            'sw': rect.move(-w,h),
            'w':  rect.move(-w,0),
            'nw': rect.move(-w,-h) }
        for edge in edges:
            current = (edges[edge][0], edges[edge][1])
            curX, curY = current
            maxX, maxY = self.get_size()
            if (0 <= curX <= maxX and 0 <= curY <= maxY and
                    current in self.position and offset in self.position):
                self.position[offset][1][edge] = self.position[current][0].type

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

        self.layers['terrain'].dirty = 1
        for layer in self.layers:
            self.layers[layer].rect.move_ip(offset)

    def set_nowalk(self, offset, size=[32,32], pos=[0,0]):
        """Sets the parts of the tile that are unwalkable."""

        rect = Rect(offset[0] + pos[0], offset[1] + pos[1], size[0], size[1])
        self.nowalk.append(rect)

    def set_above(self, width, height, tile, offset, section):
        """Draws the correct piece of the tile to the foreground."""

        if (width > self.tile_size[0]) or (height > self.tile_size[1]):
            self.layers['foreground'].image.blit(tile, offset, section)

    def set_region(self, tile, offset):
        """Sets the region number for the tile."""

        rect = Rect(offset[0], offset[1], self.tile_size[0],self.tile_size[1])
        if tile in self.regions:
            self.regions[tile].append(rect)
        else:
            self.regions[tile] = []

    def scroll(self, camera, player):
        """Scroll the map to keep the player visible."""

        b_x, b_y = player.rect.center
        camera.center = (b_x, b_y)
        b_x, b_y = camera.topleft
        camera_w, camera_h = (camera.width, camera.height)
        map_w, map_h = (self.get_size())
        if b_x < 0:
            b_x = 0
        if b_x > map_w - camera_w:
            b_x = map_w - camera_w
        if b_y < 0:
            b_y = 0
        if b_y > map_h - camera_h:
            b_y = map_h - camera_h
        if map_h < camera_h:
            b_y = (map_h - camera_h) / 2
        if map_w < camera_w:
            b_x - (map_w - camera_w) / 2
        camera.topleft = [ -b_x, -b_y ]
        self.move_map([ camera[0], camera[1] ])
        player.rect.move_ip([ camera[0], camera[1] ])
        player.scroll_pos = [ camera[0], camera[1] ]

class LayerSprite(pygame.sprite.DirtySprite):
    """Creates a map layer."""

    def __init__(self, w, numx, h, numy):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface((w * numx, h * numy), SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
