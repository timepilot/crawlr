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
        self.collide = []
        self.edges = {
            FOREST: [
                { 'n':  load_tile('edges', 'forest_edge_n'),
                  'ne': load_tile('edges', 'forest_edge_ne'),
                  'e':  load_tile('edges', 'forest_edge_e'),
                  'se': load_tile('edges', 'forest_edge_se'),
                  's':  load_tile('edges', 'forest_edge_s'),
                  'sw': load_tile('edges', 'forest_edge_sw'),
                  'w':  load_tile('edges', 'forest_edge_w'),
                  'nw': load_tile('edges', 'forest_edge_nw')
                }, True, (0,0,0,0), [32,32], [0,0] ],
            SAND: [
                { 'n':  load_tile('edges', 'dirt_edge_n'),
                  'ne': load_tile('edges', 'dirt_edge_ne'),
                  'e':  load_tile('edges', 'dirt_edge_e'),
                  'se': load_tile('edges', 'dirt_edge_se'),
                  's':  load_tile('edges', 'dirt_edge_s'),
                  'sw': load_tile('edges', 'dirt_edge_sw'),
                  'w':  load_tile('edges', 'dirt_edge_w'),
                  'nw': load_tile('edges', 'dirt_edge_nw')
                }, True, (0,0,0,0), [32,32], [0,0] ] }
        self.corners = {
            FOREST: [
                { 'ne': load_tile('edges', 'forest_corner_ne'),
                  'se': load_tile('edges', 'forest_corner_se'),
                  'sw': load_tile('edges', 'forest_corner_sw'),
                  'nw': load_tile('edges', 'forest_corner_nw')
                }, True, (0,0,0,0), [32,32], [0,0] ],
            SAND: [
                { 'ne': load_tile('edges', 'dirt_corner_ne'),
                  'se': load_tile('edges', 'dirt_corner_se'),
                  'sw': load_tile('edges', 'dirt_corner_sw'),
                  'nw': load_tile('edges', 'dirt_corner_nw')
                }, True, (0,0,0,0), [32,32], [0,0] ] }


class TerrainPlains(Terrain):

    def __init__(self, image='plains', walkable=True, danger=False):
        Terrain.__init__(self, PLAINS, 1, image, walkable, danger)
        self.details = [
            load_tile('details', 'plains_01'),
            load_tile('details', 'plains_02'),
            load_tile('details', 'plains_03'),
            load_tile('details', 'plains_04') ]
        self.objects = {
            "R1": [ load_tile('objects', 'rock_01'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "R2": [ load_tile('objects', 'rock_02'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "T1": [ load_tile('objects', 'tree_01'),
                False, (0,0,96,96), [64,32], [0,96] ],
            "T2": [ load_tile('objects', 'tree_02'),
                False, (0,0,96,96), [32,32], [32,96] ],
            "T3": [ load_tile('objects', 'tree_03'),
                False, (0,0,160,128), [64,32], [32,128] ],
            "T4": [ load_tile('objects', 'tree_04'),
                False, (0,0,32,32), [32,32], [0,32] ],
            "T5": [ load_tile('objects', 'tree_05'),
                False, (0,0,64,32), [64,32], [0,32] ],
            "T6": [ load_tile('objects', 'tree_06'),
                False, (0,0,64,32), [64,32], [0,32] ],
            "T7": [ load_tile('objects', 'tree_07'),
                True, [0,0,256,128], [32,32], [0,0] ],
            "T8": [ load_tile('objects', 'tree_08'),
                False, (0,0,0,0), [256,160], [0,0] ],
            "T9": [ load_tile('objects', 'tree_09'),
                False, (0,0,0,0), [192,32], [32,0] ],
            "B1": [ load_tile('objects', 'bush_01'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "B2": [ load_tile('objects', 'bush_02'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "B3": [ load_tile('objects', 'bush_03'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "B4": [ load_tile('objects', 'bush_04'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "B5": [ load_tile('objects', 'bush_05'),
                False, (0,0,32,32), [32,32], [0,32] ],
            "B6": [ load_tile('objects', 'bush_06'),
                False, (0,0,32,32), [32,32], [0,32] ],
            "B7": [ load_tile('objects', 'bush_07'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "B8": [ load_tile('objects', 'bush_08'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "M1": [ load_tile('objects', 'mushroom'),
                False, (0,0,0,0), [32,32], [0,0] ] }

    def draw_details(self, layer, offset):
        """Draws details on the terrain."""

        detail = choice(range(0,4))
        if Die(20).roll() >= 18:
            layer.image.blit(self.details[detail], offset)



class TerrainSand(Terrain):

    def __init__(self, image='dirt', walkable=True, danger=False):
        Terrain.__init__(self, SAND, 3, image, walkable, danger)
        self.details = [
            load_tile('details', 'plains_02'),
            load_tile('details', 'plains_03'),
            load_tile('details', 'plains_04') ]
        self.objects = {
            "R1": [ load_tile('objects', 'rock_01'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "R2": [ load_tile('objects', 'rock_02'),
                False, (0,0,0,0), [32,32], [0,0] ] }

    def draw_details(self, layer, offset):
        """Draws details on the terrain."""

        detail = choice(range(0,3))
        if Die(20).roll() >= 18:
            layer.image.blit(self.details[detail], offset)


class TerrainForest(Terrain):

    def __init__(self, image='forest', walkable=True, danger=False):
        Terrain.__init__(self, FOREST, 2, image, walkable, danger)
        self.details = [
            load_tile('details', 'forest_01'),
            load_tile('details', 'forest_02'),
            load_tile('details', 'forest_03') ]
        self.objects = {
            "R1": [ load_tile('objects', 'rock_01'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "R2": [ load_tile('objects', 'rock_02'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "T1": [ load_tile('objects', 'tree_01'),
                False, (0,0,96,96), [64,32], [0,96] ],
            "T2": [ load_tile('objects', 'tree_02'),
                False, (0,0,96,96), [32,32], [32,96] ],
            "T3": [ load_tile('objects', 'tree_03'),
                False, (0,0,160,128), [64,32], [32,128] ],
            "T4": [ load_tile('objects', 'tree_04'),
                False, (0,0,32,32), [32,32], [0,32] ],
            "T5": [ load_tile('objects', 'tree_05'),
                False, (0,0,64,32), [64,32], [0,32] ],
            "T6": [ load_tile('objects', 'tree_06'),
                False, (0,0,64,32), [64,32], [0,32] ],
            "T7": [ load_tile('objects', 'tree_07'),
                True, [0,0,256,128], [32,32], [0,0] ],
            "T8": [ load_tile('objects', 'tree_08'),
                False, (0,0,0,0), [256,160], [0,0] ],
            "T9": [ load_tile('objects', 'tree_09'),
                False, (0,0,0,0), [192,32], [32,0] ],
            "B1": [ load_tile('objects', 'bush_01'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "B2": [ load_tile('objects', 'bush_02'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "B3": [ load_tile('objects', 'bush_03'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "B4": [ load_tile('objects', 'bush_04'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "B5": [ load_tile('objects', 'bush_05'),
                False, (0,0,32,32), [32,32], [0,32] ],
            "B6": [ load_tile('objects', 'bush_06'),
                False, (0,0,32,32), [32,32], [0,32] ],
            "B7": [ load_tile('objects', 'bush_07'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "B8": [ load_tile('objects', 'bush_08'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "M1": [ load_tile('objects', 'mushroom'),
                False, (0,0,0,0), [32,32], [0,0] ] }

    def draw_details(self, layer, offset):
        """Draws details on the terrain."""

        detail = choice(range(0,3))
        if Die(20).roll() >= 18:
            layer.image.blit(self.details[detail], offset)


class TerrainWater(Terrain):

    def __init__(self, image='water', walkable=False, danger=False):
        Terrain.__init__(self, WATER, 4, image, walkable, danger)
        self.details = []
        self.objects = {}

    def draw_details(self, layer, offset):
        """Draws details on the terrain."""
        pass


class TerrainRock(Terrain):

    def __init__(self, image='rock', walkable=False, danger=False):
        Terrain.__init__(self, ROCK, 3, image, walkable, danger)
        self.details = []
        self.objects = {}

    def draw_details(self, layer, offset):
        """Draws details on the terrain."""
        pass

class TerrainBeach(Terrain):

    def __init__(self, image='beach', walkable=True, danger=False):
        Terrain.__init__(self, BEACH, 0, image, walkable, danger)
        self.details = []
        self.objects = {}

    def draw_details(self, layer, offset):
        """Draws details on the terrain."""
        pass

class TerrainIce(Terrain):

    def __init__(self, image='ice', walkable=True, danger=False):
        Terrain.__init__(self, ICE, 0, image, walkable, danger)
        self.details = []
        self.objects = {}

    def draw_details(self, layer, offset):
        """Draws details on the terrain."""
        pass


class TerrainHill(Terrain):

    def __init__(self, image='hill', walkable=True, danger=False):
        Terrain.__init__(self, HILL, 0, image, walkable, danger)
        self.details = []
        self.objects = {}

    def draw_details(self, layer, offset):
        """Draws details on the terrain."""
        pass


class TerrainMountain(Terrain):

    def __init__(self, image='mountain', walkable=True, danger=False):
        Terrain.__init__(self, MOUNTAIN, 0, image, walkable, danger)
        self.details = []
        self.objects = {}

    def draw_details(self, layer, offset):
        """Draws details on the terrain."""
        pass


class TerrainSwamp(Terrain):

    def __init__(self, image='swamp', walkable=True, danger=False):
        Terrain.__init__(self, SWAMP, 0, image, walkable, danger)
        self.details = []
        self.objects = {}

    def draw_details(self, layer, offset):
        """Draws details on the terrain."""
        pass


class TerrainJungle(Terrain):

    def __init__(self, image='jungle', walkable=True, danger=False):
        Terrain.__init__(self, JUNGLE, 0, image, walkable, danger)
        self.details = []
        self.objects = {}

    def draw_details(self, layer, offset):
        """Draws details on the terrain."""
        pass


class TerrainDesert(Terrain):

    def __init__(self, image='desert', walkable=True, danger=False):
        Terrain.__init__(self, DESERT, 0, image, walkable, danger)
        self.details = []
        self.objects = {}

    def draw_details(self, layer, offset):
        """Draws details on the terrain."""
        pass


class TerrainLava(Terrain):

    def __init__(self, image='lava', walkable=True, danger=False):
        Terrain.__init__(self, LAVA, 0, image, walkable, danger)
        self.details = []
        self.objects = {}

    def draw_details(self, layer, offset):
        """Draws details on the terrain."""
        pass


class TerrainAir(Terrain):

    def __init__(self, image='air', walkable=True, danger=False):
        Terrain.__init__(self, AIR, 0, image, walkable, danger)
        self.details = []
        self.objects = {}

    def draw_details(self, layer, offset):
        """Draws details on the terrain."""
        pass


class TerrainUnderground(Terrain):

    def __init__(self, image='underground',
    walkable=True, danger=False):
        Terrain.__init__(self, UNDERGROUND, 0, image, walkable, danger)
        self.details = []
        self.objects = {}

    def draw_details(self, layer, offset):
        """Draws details on the terrain."""
        pass


class TerrainSpace(Terrain):

    def __init__(self, image='space', walkable=True, danger=False):
        Terrain.__init__(self, SPACE, 0, image, walkable, danger)
        self.details = []
        self.objects = {}

    def draw_details(self, layer, offset):
        """Draws details on the terrain."""
        pass


class TerrainCave(Terrain):

    def __init__(self, image='cave', walkable=True, danger=False):
        Terrain.__init__(self, CAVE, 0, image, walkable, danger)
        self.details = []
        self.objects = {}

    def draw_details(self, layer, offset):
        """Draws details on the terrain."""
        pass
