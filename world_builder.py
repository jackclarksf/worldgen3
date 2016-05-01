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
        #self.category_neighbour_sweep(self.initial_seed_land)

    def world_coordinates(self):
        w_coord = list(product(range(self.x), range(self.y)))
        return w_coord

    def noise_scatter(self):
        our_choices = [0, 1]
        our_coordinates = self.world_coordinates()
        for i in our_coordinates:
            if random.choice(our_choices) == 1:
                self.initial_seed_land.append(i)
            else:
                self.initial_seed_water.append(i)

    ##### NEIGHBOUR SECTION

    def category_neighbour_sweep(self, category_to_check, other_category_to_check):
        for i in category_to_check:
            self.neighbour_checking(i, other_category_to_check, category_to_check)

    def neighbour_checking(self, input_coord, list_to_check, list_to_remove):
        upper_left = input_coord[0]-1, input_coord[1]-1
        left = input_coord[0]-1, input_coord[1]
        bottom_left = input_coord[0]-1, input_coord[1]+1

        up = input_coord[0], input_coord[1]-1
        down = input_coord[0], input_coord[1]+1

        upper_right = input_coord[0]+1, input_coord[1]-1
        right = input_coord[0]+1, input_coord[1]
        bottom_right = input_coord[0]+1, input_coord[1]+1

        check_list = [upper_left, left, bottom_left, up, down, upper_right, right, bottom_right]

        neighbour_count = 0

        for i in check_list:
            if i in list_to_check:
                neighbour_count += 1

        #print("{} has {} neighbouring water tiles".format(input_coord, neighbour_count))

        if neighbour_count > 6:
            print("Removing {}".format(input_coord))
            list_to_remove.remove(input_coord)
            list_to_check.append(input_coord)

        elif neighbour_count == 3:
            pos_neighbours = [x for x in check_list if x not in list_to_check]
            actual_neighbours = [x for x in pos_neighbours if x in self.world_coordinates()]
            if len(actual_neighbours) > 0:
                our_decision = random.choice(actual_neighbours)
                list_to_remove.remove(our_decision)
                list_to_check.append(our_decision)






###TIMING STUFF WHICH WE NEED TO USE MORE

def test_function():
    L = [i for i in range(100)]

if __name__ == '__main__':
    t = Timer("test_function()", "from __main__ import test_function")
    print(t.timeit())