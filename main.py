__author__ = 'iamja_000'
from world_builder import World

size = int(input("What is the size?"))

class Game:
    def __init__(self):
        self.tick = 0
        self.world = World(size, size)
        self.world_map = [[" " for i in range(size)] for i in range(size)]

    def iterate_map(self, times):
        land = self.world.initial_seed_land
        water = self.world.initial_seed_water
        i = 0
        while i < times:
            self.world.category_neighbour_sweep(land, water)
            self.world.add_noise_to_list(land, water)
            i += 1

    def paint_map(self):
        land = self.world.initial_seed_land
        for i in land:
            self.world_map[i[1]][i[0]] = " "
        water = self.world.initial_seed_water
        for i in water:
            self.world_map[i[1]][i[0]] = "W"

    def print_map(self):
        for i in self.world_map:
            print(i)



game_world = Game()

game_world.paint_map()
game_world.print_map()
