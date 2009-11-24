from random import choice
from constants import *
from data import load_tile
from dice import Die

class Terrain(object):
    """Terrain on the world map."""

    def __init__(self, type, order, image, walkable, danger):
        self.type = type
        self.order = order
        self.image = load_tile('terrain', image)
        self.walkable = walkable
        self.danger = danger
        self.size = [32,32]
        self.collide = []
        self.edges = {
            TERRAIN_CAVE_FLOOR[0]: [
                { 's':  load_tile('edges', 'cave_floor_edge_s'),
                }, True, (0,0,0,0), [32,32], [0,0] ],
            TERRAIN_GRASS[1]: [
                { 'n':  load_tile('edges', 'grass1_edge_n'),
                  'ne': load_tile('edges', 'grass1_edge_ne'),
                  'e':  load_tile('edges', 'grass1_edge_e'),
                  'se': load_tile('edges', 'grass1_edge_se'),
                  's':  load_tile('edges', 'grass1_edge_s'),
                  'sw': load_tile('edges', 'grass1_edge_sw'),
                  'w':  load_tile('edges', 'grass1_edge_w'),
                  'nw': load_tile('edges', 'grass1_edge_nw')
                }, True, (0,0,0,0), [32,32], [0,0] ],
            TERRAIN_GRASS[2]: [
                { 'n':  load_tile('edges', 'grass2_edge_n'),
                  'ne': load_tile('edges', 'grass2_edge_ne'),
                  'e':  load_tile('edges', 'grass2_edge_e'),
                  'se': load_tile('edges', 'grass2_edge_se'),
                  's':  load_tile('edges', 'grass2_edge_s'),
                  'sw': load_tile('edges', 'grass2_edge_sw'),
                  'w':  load_tile('edges', 'grass2_edge_w'),
                  'nw': load_tile('edges', 'grass2_edge_nw')
                }, True, (0,0,0,0), [32,32], [0,0] ],
            TERRAIN_FOREST[0]: [
                { 'n':  load_tile('edges', 'forest_edge_n'),
                  'ne': load_tile('edges', 'forest_edge_ne'),
                  'e':  load_tile('edges', 'forest_edge_e'),
                  'se': load_tile('edges', 'forest_edge_se'),
                  's':  load_tile('edges', 'forest_edge_s'),
                  'sw': load_tile('edges', 'forest_edge_sw'),
                  'w':  load_tile('edges', 'forest_edge_w'),
                  'nw': load_tile('edges', 'forest_edge_nw')
                }, True, (0,0,0,0), [32,32], [0,0] ] }
        self.corners = {
            TERRAIN_GRASS[1]: [
                { 'ne': load_tile('edges', 'grass1_corner_ne'),
                  'se': load_tile('edges', 'grass1_corner_se'),
                  'sw': load_tile('edges', 'grass1_corner_sw'),
                  'nw': load_tile('edges', 'grass1_corner_nw')
                }, True, (0,0,0,0), [32,32], [0,0] ],
            TERRAIN_GRASS[2]: [
                { 'ne': load_tile('edges', 'grass2_corner_ne'),
                  'se': load_tile('edges', 'grass2_corner_se'),
                  'sw': load_tile('edges', 'grass2_corner_sw'),
                  'nw': load_tile('edges', 'grass2_corner_nw')
                }, True, (0,0,0,0), [32,32], [0,0] ],
            TERRAIN_FOREST[0]: [
                { 'ne': load_tile('edges', 'forest_corner_ne'),
                  'se': load_tile('edges', 'forest_corner_se'),
                  'sw': load_tile('edges', 'forest_corner_sw'),
                  'nw': load_tile('edges', 'forest_corner_nw')
                }, True, (0,0,0,0), [32,32], [0,0] ] }
        self.objects = {
            "a": [ load_tile('objects', 'rock_01'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "b": [ load_tile('objects', 'rock_02'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "c": [ load_tile('objects', 'tree_01'),
                False, (0,0,96,96), [64,32], [0,96] ],
            "d": [ load_tile('objects', 'tree_02'),
                False, (0,0,96,96), [32,32], [32,96] ],
            "e": [ load_tile('objects', 'tree_03'),
                False, (0,0,160,128), [64,32], [32,128] ],
            "f": [ load_tile('objects', 'tree_04'),
                False, (0,0,32,32), [32,32], [0,32] ],
            "g": [ load_tile('objects', 'tree_05'),
                False, (0,0,64,32), [64,32], [0,32] ],
            "h": [ load_tile('objects', 'tree_06'),
                False, (0,0,64,32), [64,32], [0,32] ],
            "i": [ load_tile('objects', 'tree_07'),
                True, [0,0,256,128], [32,32], [0,0] ],
            "j": [ load_tile('objects', 'tree_08'),
                False, (0,0,0,0), [256,160], [0,0] ],
            "k": [ load_tile('objects', 'tree_09'),
                False, (0,0,0,0), [192,32], [32,0] ],
            "l": [ load_tile('objects', 'bush_01'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "m": [ load_tile('objects', 'bush_02'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "n": [ load_tile('objects', 'bush_03'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "o": [ load_tile('objects', 'bush_04'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "p": [ load_tile('objects', 'bush_05'),
                False, (0,0,32,32), [32,32], [0,32] ],
            "q": [ load_tile('objects', 'bush_06'),
                False, (0,0,32,32), [32,32], [0,32] ],
            "r": [ load_tile('objects', 'bush_07'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "s": [ load_tile('objects', 'bush_08'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "t": [ load_tile('objects', 'mushroom'),
                False, (0,0,0,0), [32,32], [0,0] ] }


class TerrainCaveCeiling(Terrain):

    def __init__(self, image='cave_ceiling', walkable=True, danger=False):
        Terrain.__init__(self, TERRAIN_CAVE_CEILING[0], 1, image, walkable,
            danger)
        self.size = [64,32]
        self.details = [
            load_tile('details', 'cave_ceiling_01'),
            load_tile('details', 'cave_ceiling_02'),
            load_tile('details', 'cave_ceiling_03') ]

    def draw_details(self, layer, offset):
        """Draws details on the terrain."""

        detail = choice(range(0,3))
        if Die(20).roll() >= 18:
            layer.image.blit(self.details[detail], offset)


class TerrainCaveFloor(Terrain):

    def __init__(self, image='cave_floor', walkable=True, danger=False):
        Terrain.__init__(self, TERRAIN_CAVE_FLOOR[0], 2, image, walkable,
            danger)

    def draw_details(self, layer, offset):
        """Draws details on the terrain."""

        pass


class TerrainGrass(Terrain):

    def __init__(self, image, walkable=True, danger=False):
        terrain = TERRAIN_GRASS[image]
        image = 'grass' + str(image)
        Terrain.__init__(self, terrain, 1, image, walkable, danger)
        self.details = [
            load_tile('details', 'grass_01'),
            load_tile('details', 'grass_02'),
            load_tile('details', 'grass_03'),
            load_tile('details', 'grass_04') ]

    def draw_details(self, layer, offset):
        """Draws details on the terrain."""

        detail = choice(range(0,4))
        if Die(20).roll() >= 18:
            layer.image.blit(self.details[detail], offset)


class TerrainForest(Terrain):

    def __init__(self, image='forest', walkable=True, danger=False):
        Terrain.__init__(self, TERRAIN_FOREST[0], 2, image, walkable, danger)
        self.details = [
            load_tile('details', 'forest_01'),
            load_tile('details', 'forest_02'),
            load_tile('details', 'forest_03') ]

    def draw_details(self, layer, offset):
        """Draws details on the terrain."""

        detail = choice(range(0,3))
        if Die(20).roll() >= 18:
            layer.image.blit(self.details[detail], offset)
