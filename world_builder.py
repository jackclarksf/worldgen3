__author__ = 'iamja_000'

from itertools import product, starmap
import random
from timeit import Timer
from world_map import WorldMap
from entities import City

class World:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.cities = []
        self.our_map = WorldMap(x, y)
        self.our_world_map = self.our_map.map_display_list()
        self.initial_seed_land = self.our_map.initial_seed_land
        self.initial_seed_water = self.our_map.initial_seed_water
        self.city_scatter(round(self.x/3))

    def map_get(self):
        return self.our_world_map

    def city_scatter(self, number_of_cities):
        i = 0
        while i < number_of_cities:
            city_locations_and_neighbours = self.get_all_entity_neighbours(self.cities, 2)
            possible_coordinate = random.choice([x for x in self.initial_seed_land if x not in city_locations_and_neighbours])
            while possible_coordinate in city_locations_and_neighbours:
                possible_coordinate = random.choice(self.initial_seed_land)
            self.cities.append(City(possible_coordinate[0], possible_coordinate[1], possible_coordinate[0], possible_coordinate[1]))
            i += 1
        self.paint_map_with_entities(self.our_world_map)
        #NEXT STEP = ADD AWARENESS OF CITY SPACE/BORDER

    def get_entity_locations(self, entity_type):
        coordinate_list = []
        for i in entity_type:
            coordinate = i.get_location()
            coordinate_list.append(coordinate)
        return coordinate_list

    def paint_map_with_entities(self, map_to_paint):
        city_locs = self.get_entity_locations(self.cities)
        for i in city_locs:
            self.our_world_map[i[1]][i[0]] = "C"

#### NEIGHBOUR FUNCTIONS

    def get_all_entity_neighbours(self, entity_list, radius):
        total_list = []
        for i in entity_list:
            our_location = i.get_location()
            extension = self.get_neighbours_specifiable(our_location[0], our_location[1], radius)
            total_list.extend(extension)
        return total_list

    def get_neighbours_specifiable(self, x_coord, y_coord, radius):
        r_list = []
        for i in range(-radius, radius+1):
            r_list.append(i)
        cells = starmap(lambda a,b: (x_coord+a, y_coord+b), product((r_list), (r_list)))
        return list(cells)[1:]

    def neighbour_type_check_return(self, x, y, distance_to_check, entity_coordinates):
        neighbour_list = [x for x in self.get_neighbours_specifiable(x, y, distance_to_check) if x in entity_coordinates]
        return neighbour_list




###TIMING STUFF WHICH WE NEED TO USE MORE

def test_function():
    L = [i for i in range(100)]

if __name__ == '__main__':
    t = Timer("test_function()", "from __main__ import test_function")
    print(t.timeit())