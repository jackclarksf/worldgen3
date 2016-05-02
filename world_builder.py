__author__ = 'iamja_000'

from itertools import product
import random
from timeit import Timer

class World:
    def __init__(self, x, y):
        self.initial_seed_land = []
        self.initial_seed_water = []
        self.x = int(x)
        self.y = int(y)
        self.noise_scatter()
        iter_count = 0

        while len(self.initial_seed_land) < (((len(self.world_coordinates()))/2)+ (self.x/4)):
            print(len(self.initial_seed_land))
            print((len(self.world_coordinates()))/2)
            self.category_neighbour_sweep(self.initial_seed_land, self.initial_seed_water)
            self.add_noise_to_list(self.initial_seed_water, self.initial_seed_land)
            iter_count += 1
        print("That took: {}".format(iter_count))

        if iter_count < 3:
            self.category_neighbour_sweep(self.initial_seed_land, self.initial_seed_water)
            iter_count += 1

        print("That took: {}".format(iter_count))

    def world_coordinates(self):
        w_coord = list(product(range(self.x), range(self.y)))
        return w_coord

    ####NOISE FUNCTIONS

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
            else:
                self.initial_seed_water.append(i)

    ##### NEIGHBOUR SECTION

    def category_neighbour_sweep(self, land_category, water_category):
        for i in self.world_coordinates():
            self.neighbour_checking(i, land_category, water_category)

    def neighbour_checking(self, input_coord, land_list, water_list):
        upper_left = input_coord[0]-1, input_coord[1]-1
        left = input_coord[0]-1, input_coord[1]
        bottom_left = input_coord[0]-1, input_coord[1]+1

        up = input_coord[0], input_coord[1]-1
        down = input_coord[0], input_coord[1]+1

        upper_right = input_coord[0]+1, input_coord[1]-1
        right = input_coord[0]+1, input_coord[1]
        bottom_right = input_coord[0]+1, input_coord[1]+1

        check_list = [upper_left, left, bottom_left, up, down, upper_right, right, bottom_right]

        land_neighbour_count = 0
        water_neighbour_count = 0

        if input_coord in land_list:
            our_type = land_list
        else:
            our_type = water_list

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


        #print("{} has {} neighbouring water tiles and {} neighbouring land tiles".format(input_coord, land_neighbour_count, water_neighbour_count))









###TIMING STUFF WHICH WE NEED TO USE MORE

def test_function():
    L = [i for i in range(100)]

if __name__ == '__main__':
    t = Timer("test_function()", "from __main__ import test_function")
    print(t.timeit())