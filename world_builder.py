__author__ = 'iamja_000'

from itertools import product, starmap
import random
from timeit import Timer
from world_map import WorldMap
from entities import City, Scout

##IMPLEMENT A WAY TO COUNT SIZE OF ROOMS SO AS TO AVOID PUTTING CITIES IN WEIRD SPOTS

class World:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.cities = []
        self.scouts = []
        self.roads = []
        self.our_map = WorldMap(x, y)
        self.our_world_map = self.our_map.map_display_list()
        self.initial_seed_land = self.our_map.initial_seed_land
        self.initial_seed_water = self.our_map.initial_seed_water
        self.city_scatter(round(self.x/3))
        self.city_spawn()

    def map_get(self):
        return self.our_world_map

    def alt_map_get(self):
        world_map = [[" " for i in range(self.x)] for i in range(self.y)]
        for i in self.initial_seed_land:
            world_map[i[1]][i[0]] = " "
        for i in self.initial_seed_water:
            world_map[i[1]][i[0]] = "W"
        for i in self.scouts:
            j = i.get_location()
            world_map[j[1]][j[0]] = "S"
        path_list = self.scout_path_list()
        for i in path_list:
            x, y = i
            world_map[y][x] = "P"
        for i in self.cities:
            j = i.get_location()
            world_map[j[1]][j[0]] = "C"
        return world_map

    def scout_path_list(self):
        self.meta_paths = []
        for i in self.scouts:
            the_path = list(i.return_paths())
            slim_path = list(set(the_path))
            self.meta_paths.extend(slim_path)
        slimmed_meta = list(set(self.meta_paths))
        neatened = sorted(slimmed_meta)
        return neatened



    def get_room_size(self, map_to_check, x, y, old_character, new_character, count):

        if map_to_check[y][x] != old_character:
            total_length = len(count)
            print("Weirdo length = {}".format(total_length))
            return total_length
        map_to_check[y][x] = new_character
        count.append(new_character)

        if x > 0: # left
            self.get_room_size(map_to_check, x-1, y, old_character, new_character, count)

        if y > 0: # up
            self.get_room_size(map_to_check, x, y-1, old_character, new_character, count)

        if x < self.x-1: # right
            self.get_room_size(map_to_check, x+1, y, old_character, new_character, count)

        if y < self.y-1: # down
            self.get_room_size(map_to_check, x, y+1, old_character, new_character, count)


    def city_scatter(self, number_of_cities):
        i = 0
        while i < number_of_cities:
            city_locations_and_neighbours = self.get_all_entity_neighbours(self.cities, (round(self.x/4)))
            too_much_water_coord = []
            for j in self.initial_seed_land:
                near_water = (self.neighbour_type_check_return(j[0], j[1], 1, self.initial_seed_water))
                if ((len(near_water))+1)>4:
                    too_much_water_coord.append(j)
            land_options1 = [x for x in self.initial_seed_land if x not in too_much_water_coord]
            land_options = [x for x in land_options1 if x not in city_locations_and_neighbours]
            if len(land_options) > 0:
                possible_coordinate = random.choice(land_options)
                print("Pos coordinate chosen = {}".format(possible_coordinate))
                #island_size = self.get_room_size(self.our_world_map, possible_coordinate[0], possible_coordinate[1], " ", "$", [])
                #print("Size of island: {}".format(len(island_size)))
                self.cities.append(City(possible_coordinate[0], possible_coordinate[1], possible_coordinate[0], possible_coordinate[1]))
                i += 1
            else:
                print("Done")
                i += 1
        #self.paint_map_with_entities(self.our_world_map)

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

#####SPAWN FUNCTIONS

    def city_spawn(self):
        for i in self.cities:
            loc = i.get_location()
            pos_points = self.neighbour_type_check_return(loc[0], loc[1], 1, self.initial_seed_land)
            pos_points.remove(loc)
            our_scout = random.choice(pos_points)
            self.scouts.append(Scout(our_scout[0], our_scout[1], loc[0], loc[1]))


####LOCATION FUNCTIONS
    def location_list(self, entity_type):
        entity_list = []
        for i in entity_type:
            loc = i.get_location()
            entity_list.append(loc)
        return entity_list

    def return_object_from_location(self, entity_type, location_a, location_b):
        for i in entity_type:
            if i.get_location() == (location_a, location_b):
                return i

######MOVEMENT FUNCTIONS
        #EACH MOVEMENT FUNCTION MUST BE ACCOMPANIED BY A CITY SCOUTING FUNCTION

    def scout_movement(self):
        for i in self.scouts:
            i_loc = i.get_location()
            pos_moves = self.neighbour_type_check_return(i_loc[0], i_loc[1], 1, self.initial_seed_land)
            self.scout_scanner(i, i_loc)
            #CITY SCANNER GOES HERE
            if len(pos_moves) > 0:
                i.paths_taken.append(i_loc)
                our_move = random.choice(pos_moves)
                i.x = our_move[0]
                i.y = our_move[1]

    def scout_scanner(self, scout, scout_location):
        #GET CITY LOCATIONS
        city_locations = self.location_list(self.cities)
        #print("Scout scanner {}".format(city_locations))
        #CHECK IF A CITY COORDINATE IS NEARBY
        potential_collision = self.neighbour_type_check_return(scout_location[0], scout_location[1], 1, city_locations)
        #print("Possible cities: {}".format(potential_collision))
        if len(potential_collision) > 0:
            collision_coordinate = potential_collision[0][0], potential_collision[0][1]
            print("City location: {}".format(collision_coordinate))
            potential_city = self.return_object_from_location(self.cities, collision_coordinate[0], collision_coordinate[1])
            orig_a, orig_b = potential_city.return_city_origin()
            print("City origination point: {} {}".format(orig_a, orig_b))

        #IF NEARBY, CHECK SCOUT ORIGIN AGAINST CITY
            origin = scout.x0, scout.y0
            #print("Scout origin: {}".format(origin))
            if origin in potential_collision:
                #print("Duplicate...removing")
                potential_collision.remove(origin)
                #print("Collisions now: {}".format(potential_collision))
                if len(potential_collision) > 0:
                    #print("Looks like we are good to go!")
                    self.cities.append((City(scout.x, scout.y, collision_coordinate[0], collision_coordinate[1])))
                    #print("Killing scout at location {} {}".format(scout.x, scout.y))
                    print("Creating a road here, son!")
                    our_paths = list(scout.return_paths())
                    slimmed_path = list(set(our_paths))
                    print("Scout paths: {}".format(slimmed_path))
                    #FIND PATH ENTITY CLOSEST TO LOCATION
                    #self.roads.append((Road()))
                    self.scouts.remove(scout)
            else:
                print("Looks like we are good to go!")
                self.cities.append((City(scout.x, scout.y, collision_coordinate[0], collision_coordinate[1])))
                print("Killing scout at location {} {}".format(scout.x, scout.y))
                self.scouts.remove(scout)



#####MOVEMENT FUNCTIONS








###TIMING STUFF WHICH WE NEED TO USE MORE

def test_function():
    L = [i for i in range(100)]

if __name__ == '__main__':
    t = Timer("test_function()", "from __main__ import test_function")
    print(t.timeit())