__author__ = 'iamja_000'

class City:
    def __init__(self, x, y, origin_a, origin_b):
        self.x = x
        self.y = y
        self.x0 = origin_a
        self.y0 = origin_b
        self.growth = 0
        self.age = 0
        self.energy = 0
        #print("CITY BORN AT X: {} Y: {} \n Origin X: {} Y: {}".format(self.x, self.y, self.x0, self.y0))

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

    def get_location(self):
        return self.x, self.y

    def return_city_origin(self):
        return self.x0, self.y0

