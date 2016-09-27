__author__ = 'iamja_000'
from world_builder import World

size = int(input("What is the size?"))

class Game:
    def __init__(self):
        self.tick = 0
        self.world = World(size, size)
        self.world_map = [[" " for i in range(size)] for i in range(size)]
        #self.world_real_map = self.world.alt_map_get()

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

    def alt_print(self):
        self.world_real_map = self.world.alt_map_get()
        for i in self.world_real_map:
            print(i)

    def tick_forward(self):
        print(self.tick)
        self.tick += 1


    def map_step(self):
        self.world.proximity_check()
        self.world.city_spawn_check()
        self.world.scout_movement()
        self.world.print_state()
        #self.world.city_origin_print()
        self.world.city_location_print()
        game_world.alt_print()
        self.tick_forward()



game_world = Game()

while game_world.tick < 200:
    #y_check = input("Tick?")
    #if y_check == "y":
    #    game_world.map_step()
    game_world.map_step()

#game_world.paint_map()
#game_world.print_map()

#next big idea needed = how do we stop cities growing perpetually? probably by using nearby resources.
## eg, land has a base resource level of 10 that can be drained by cities.
#if it drains to zero then it lies fallow for time until it refilles.
