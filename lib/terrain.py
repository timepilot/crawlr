from random import choice
from constants import *
from data import load_image
from dice import Die

class Terrain(object):
    """Terrain on the world map."""

    def __init__(self, type, order, image_name, image, num_details,
            freq_details, walkable=True, danger=False):
        self.type = type
        self.order = order
        self.image_name = image_name
        self.image = load_image('map', 'terrain', image)
        self.num_details = num_details
        self.freq_details = freq_details
        self.walkable = walkable
        self.danger = danger
        self.collide = []
        self.edges = {
            TERRAIN_GRASS[1]: {
                'n':  load_image('map', 'edges', 'grass1_edge_n'),
                'ne': load_image('map', 'edges', 'grass1_edge_ne'),
                'e':  load_image('map', 'edges', 'grass1_edge_e'),
                'se': load_image('map', 'edges', 'grass1_edge_se'),
                's':  load_image('map', 'edges', 'grass1_edge_s'),
                'sw': load_image('map', 'edges', 'grass1_edge_sw'),
                'w':  load_image('map', 'edges', 'grass1_edge_w'),
                'nw': load_image('map', 'edges', 'grass1_edge_nw') },
            TERRAIN_GRASS[2]: {
                'n':  load_image('map', 'edges', 'grass2_edge_n'),
                'ne': load_image('map', 'edges', 'grass2_edge_ne'),
                'e':  load_image('map', 'edges', 'grass2_edge_e'),
                'se': load_image('map', 'edges', 'grass2_edge_se'),
                's':  load_image('map', 'edges', 'grass2_edge_s'),
                'sw': load_image('map', 'edges', 'grass2_edge_sw'),
                'w':  load_image('map', 'edges', 'grass2_edge_w'),
                'nw': load_image('map', 'edges', 'grass2_edge_nw') },
            TERRAIN_FOREST[0]: {
                'n':  load_image('map', 'edges', 'forest_edge_n'),
                'ne': load_image('map', 'edges', 'forest_edge_ne'),
                'e':  load_image('map', 'edges', 'forest_edge_e'),
                'se': load_image('map', 'edges', 'forest_edge_se'),
                's':  load_image('map', 'edges', 'forest_edge_s'),
                'sw': load_image('map', 'edges', 'forest_edge_sw'),
                'w':  load_image('map', 'edges', 'forest_edge_w'),
                'nw': load_image('map', 'edges', 'forest_edge_nw') }
            }
        self.corners = {
            TERRAIN_GRASS[1]: {
                'ne': load_image('map', 'edges', 'grass1_corner_ne'),
                'se': load_image('map', 'edges', 'grass1_corner_se'),
                'sw': load_image('map', 'edges', 'grass1_corner_sw'),
                'nw': load_image('map', 'edges', 'grass1_corner_nw') },
            TERRAIN_GRASS[2]: {
                'ne': load_image('map', 'edges', 'grass2_corner_ne'),
                'se': load_image('map', 'edges', 'grass2_corner_se'),
                'sw': load_image('map', 'edges', 'grass2_corner_sw'),
                'nw': load_image('map', 'edges', 'grass2_corner_nw') },
            TERRAIN_FOREST[0]: {
                'ne': load_image('map', 'edges', 'forest_corner_ne'),
                'se': load_image('map', 'edges', 'forest_corner_se'),
                'sw': load_image('map', 'edges', 'forest_corner_sw'),
                'nw': load_image('map', 'edges', 'forest_corner_nw') }
            }

    def draw_details(self, layer, offset):
        """Draw details on the terrain."""

        if self.num_details > 0:
            detail = choice(range(1, self.num_details+1))
            if Die(20).roll() >= self.freq_details:
                tile = load_image('map', 'details', self.image_name + str(detail))
                layer.image.blit(tile, offset)


class TerrainGrass(Terrain):

    def __init__(self, num, image='grass'):
        terrain = TERRAIN_GRASS[num]
        num_details = 4
        freq_details = 18
        Terrain.__init__(self, terrain, 1, image, image + str(num),
            num_details, freq_details)
        self.objects = {
            "a": [ load_image('map', 'objects', 'rock_01'),
                False, (0,0,0,0), [20,20], [6,6] ],
            "b": [ load_image('map', 'objects', 'rock_02'),
                False, (0,0,0,0), [22,16], [6,4] ],
            "c": [ load_image('map', 'objects', 'tree_04'),
                False, (0,0,32,32), [32,32], [0,32] ],
            "d": [ load_image('map', 'objects', 'tree_05'),
                False, (0,0,64,32), [64,32], [0,32] ],
            "e": [ load_image('map', 'objects', 'tree_06'),
                False, (0,0,64,32), [64,32], [0,32] ] }


class TerrainForest(Terrain):

    def __init__(self, num, image='forest'):
        terrain = TERRAIN_FOREST[num]
        num_details = 3
        freq_details = 10
        Terrain.__init__(self, terrain, 2, image, image + str(num),
            num_details, freq_details)
        self.objects = {
            "a": [ load_image('map', 'objects', 'tree_01'),
                False, (0,0,96,96), [64,32], [0,96] ],
            "b": [ load_image('map', 'objects', 'tree_02'),
                False, (0,0,96,96), [40,32], [27,96] ],
            "c": [ load_image('map', 'objects', 'tree_03'),
                False, (0,0,160,128), [64,32], [32,128] ],
            "d": [ load_image('map', 'objects', 'tree_07'),
                False, [0,0,256,128], [32,32], [0,0] ],
            "e": [ load_image('map', 'objects', 'tree_08'),
                False, (0,0,0,0), [256,160], [0,0] ],
            "f": [ load_image('map', 'objects', 'tree_09'),
                False, (0,0,0,0), [192,32], [32,0] ],
            "g": [ load_image('map', 'objects', 'bush_01'),
                True, (0,0,0,0), [32,32], [0,0] ],
            "h": [ load_image('map', 'objects', 'bush_02'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "i": [ load_image('map', 'objects', 'bush_03'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "j": [ load_image('map', 'objects', 'bush_04'),
                False, (0,0,0,0), [32,32], [0,0] ],
            "k": [ load_image('map', 'objects', 'bush_05'),
                False, (0,0,32,32), [32,32], [0,32] ],
            "l": [ load_image('map', 'objects', 'bush_06'),
                False, (0,0,32,32), [32,32], [0,32] ],
            "m": [ load_image('map', 'objects', 'bush_07'),
                False, (0,0,64,32), [64,32], [0,32] ],
            "n": [ load_image('map', 'objects', 'bush_08'),
                False, (0,0,64,32), [96,32], [0,32] ],
            "o": [ load_image('map', 'objects', 'mushroom'),
                True, (0,0,0,0), [32,32], [0,0] ] }
