__author__ = 'iamja_000'

from itertools import product, starmap
import random
from timeit import Timer
from world_map import WorldMap

class World:
    def __init__(self, x, y):
        self.initial_seed_land = []
        self.initial_seed_water = []
        self.x = int(x)
        self.y = int(y)
        self.our_map = WorldMap(x, y)
        self.our_world_map = self.our_map.map_display_list()

    def map_get(self):
        return self.our_world_map


###TIMING STUFF WHICH WE NEED TO USE MORE

def test_function():
    L = [i for i in range(100)]

if __name__ == '__main__':
    t = Timer("test_function()", "from __main__ import test_function")
    print(t.timeit())