__author__ = 'iamja_000'

import random

class City:
    def __init__(self, x, y, origin_a, origin_b):
        self.x = x
        self.y = y
        self.x0 = origin_a
        self.y0 = origin_b
        self.growth = 0
        self.age = 0
        self.energy = 0
        print("CITY BORN AT X: {} Y: {} \n Origin X: {} Y: {}".format(self.x, self.y, self.x0, self.y0))

    def add_growth(self):
        self.growth += 1
        #print("ADDED GROWTH to city at {} {} with origin {} {}. Growth now {}".format(self.x, self.y, self.x0, self.y0, self.growth))

    def get_location(self):
        return self.x, self.y

    def return_city_origin(self):
        return self.x0, self.y0

    def add_age(self):
        self.age += 1

class Scout:
    def __init__(self, x, y, origin_a, origin_b):
        self.x = x
        self.y = y
        self.x0 = origin_a
        self.y0 = origin_b
        self.paths_taken = []
        start_loc = self.x, self.y
        self.paths_taken.append(start_loc)

    def return_paths(self):
        return self.paths_taken

    def get_location(self):
        return self.x, self.y


    def return_city_origin(self):
        return self.x0, self.y0

class Road:

    def __init__(self, x, y, origin_a, origin_b, end_city_location, path_log):
        Scout.__init__(self, x, y, origin_a, origin_b)
        self.end_city = end_city_location
        self.original_path = path_log
        print("Road born at AT X: {} Y: {} \n connecting city X: {} Y: {} with city {}".format(self.x, self.y, origin_a, origin_b, end_city_location))

    def return_end_city(self):
        return self.end_city

    def return_original_path(self):
        return self.original_path
    ##entities can use cities as pass-through coordinates to join two separate road routes
    ##entities have a bias for longer routes as they carry more value
    ##entities move and shift random (1-2) per turn
    ##entities speed grows slowly as cities age

class Land:
    def __init__(self, x, y):
        energy = [5, 6, 7, 8, 9, 20]
        self.x = x
        self.y = y
        self.resource = random.choice(energy)

    def get_location(self):
        return self.x, self.y

    def harvest(self):
        self.resource -= 1



