__author__ = 'iamja_000'


__author__ = 'iamja_000'

from itertools import product, starmap
import random
from timeit import Timer
from entities import Land

class WorldMap:
    def __init__(self, x, y):
        self.object_land = []
        self.initial_seed_land = self.land_coordinates(self.object_land)
        #self.initial_seed_land = []
        self.initial_seed_water = []
        self.x = int(x)
        self.y = int(y)
        iter_count = 0

        self.noise_scatter()

        while len(self.initial_seed_land) < (((len(self.world_coordinates()))/2) + (len(self.world_coordinates())/4)):
            print(len(self.initial_seed_land))
            print((len(self.world_coordinates()))/2)
            self.category_neighbour_sweep(self.initial_seed_land, self.initial_seed_water)
            self.add_noise_to_list(self.initial_seed_water, self.initial_seed_land)
            iter_count += 1

        if iter_count < 3:
            self.category_neighbour_sweep(self.initial_seed_land, self.initial_seed_water)
            iter_count += 1

        print("That took: {}".format(iter_count))
        print("Trying our borders now")
        self.border_creator(self.world_coordinates(), self.initial_seed_land, self.initial_seed_water)

        get_a_map = self.map_display_list()
        #self.base_flood_fill_algorithm(get_a_map, 0, 4, " ", "$")
        room_count = self.count_rooms(get_a_map)
        print("Total number of rooms: {}".format(room_count))
        self.hole_punch()
        while room_count > 6:
            self.category_neighbour_sweep(self.initial_seed_land, self.initial_seed_water)
            get_a_map = self.map_display_list()
            room_count = self.count_rooms(get_a_map)
            print("Room count now: {}".format(room_count))
            #MAYBE ADD SOMETHING TO RANDOMLY DELETE SOME WATER AND REPLACE WITH LAND?
            iter_count += 1
            if iter_count > 10:
                self.add_noise_to_list(self.initial_seed_water, self.initial_seed_land)
                iter_count -= 10
        print("That took: {}".format(iter_count))


        #return self.map_display_list()

    def land_coordinates(self, entity_list):
        co_ord = []
        for i in entity_list:
            location = i.get_location()
            co_ord.append(location)
        return co_ord

    def world_coordinates(self):
        w_coord = list(product(range(self.x), range(self.y)))
        return w_coord

    def border_creator(self, world_co, land_list, water_list):
        the_new_borders = []
        for i in world_co:
            a, b, = i
            if a == 0:
                the_new_borders.append(i)
            elif b == 0:
                the_new_borders.append(i)
            elif a == self.x-1:
                the_new_borders.append(i)
            elif b == self.y-1:
                the_new_borders.append(i)
        self.initial_seed_land = [x for x in land_list if x not in the_new_borders]
        water_list.extend(the_new_borders)


    #NOISE FUNCTIONS

    def add_noise_to_list(self, possible_coordinates, list_to_add_to):
        choices = [0, 1, 2, 3, 4, 5]
        for i in possible_coordinates:
            fill_chance = random.choice(choices)
            if fill_chance == 5:
                possible_coordinates.remove(i)
                list_to_add_to.append(i)

    def noise_scatter(self):
        our_choices = [0, 1]
        our_coordinates = self.world_coordinates()
        for i in our_coordinates:
            if random.choice(our_choices) == 1:
                self.initial_seed_land.append(i)
                self.object_land.append(Land(i[0], i[1]))
                #ATTEMPING LAND ADDITION HERE
            else:
                self.initial_seed_water.append(i)

    ##### NEIGHBOUR SECTION

    def get_neighbours_specifiable(self, x_coord, y_coord, radius):
        r_list = []
        for i in range(-radius, radius+1):
            r_list.append(i)
        cells = starmap(lambda a,b: (x_coord+a, y_coord+b), product((r_list), (r_list)))
        return list(cells)[1:]

    def category_neighbour_sweep(self, land_category, water_category):
        for i in self.world_coordinates():
            self.neighbour_checking(i, land_category, water_category)

    def neighbour_checking(self, input_coord, land_list, water_list):

        check_list = self.get_neighbours_specifiable(input_coord[0], input_coord[1], 1)

        land_neighbour_count = 0
        water_neighbour_count = 0

        for i in check_list:
            if i in land_list:
                land_neighbour_count += 1
            elif i in water_list:
                water_neighbour_count += 1

        if input_coord in water_list and water_neighbour_count > 3:
            pass
        elif input_coord in land_list and land_neighbour_count > 3:
            pass

        elif input_coord in water_list and land_neighbour_count > 4:
            water_list.remove(input_coord)
            land_list.append(input_coord)
        elif input_coord in land_list and water_neighbour_count > 4:
            land_list.remove(input_coord)
            water_list.append(input_coord)


    def map_display_list(self):
        world_map = [[" " for i in range(self.x)] for i in range(self.y)]
        for i in self.initial_seed_land:
            world_map[i[1]][i[0]] = " "
        for i in self.initial_seed_water:
            world_map[i[1]][i[0]] = "W"
        return world_map

    def base_flood_fill_algorithm(self, world_map, x, y, old_character, new_character):

        if world_map[y][x] != old_character:
            return
        world_map[y][x] = new_character


        if x > 0: # left
            self.base_flood_fill_algorithm(world_map, x-1, y, old_character, new_character)

        if y > 0: # up
            self.base_flood_fill_algorithm(world_map, x, y-1, old_character, new_character)

        if x < self.x-1: # right
            self.base_flood_fill_algorithm(world_map, x+1, y, old_character, new_character)

        if y < self.y-1: # down
            self.base_flood_fill_algorithm(world_map, x, y+1, old_character, new_character)

    def count_rooms(self, world_map):
        roomCount = 0
        for x in range(self.x):
            for y in range(self.y):
                if world_map[y][x] == " ":
                    self.base_flood_fill_algorithm(world_map, x, y, " ", "$")

                    roomCount += 1
        #for i in world_map:
        #    print(i)
        return roomCount

    def hole_punch(self):
        global_coord = self.world_coordinates()
        our_length = len(global_coord)
        our_water_radius = round(our_length/6)
        #for i in global_coord[our_water_radius:our_length-our_water_radius]:
            #print(i)
        #NEXT STEP, USE THIS TO CREATE HOLES IN IT ETC



###TIMING STUFF WHICH WE NEED TO USE MORE

def test_function():
    L = [i for i in range(100)]

if __name__ == '__main__':
    t = Timer("test_function()", "from __main__ import test_function")
    print(t.timeit())