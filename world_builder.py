__author__ = 'iamja_000'

from itertools import product, starmap
import random
from timeit import Timer
from world_map import WorldMap
from entities import City, Scout, Road, Land
import implementation

#CITY ORIGIN LOOP IS FUCKED UP, SON
##IMPLEMENT A WAY TO COUNT SIZE OF ROOMS SO AS TO AVOID PUTTING CITIES IN WEIRD SPOTS

class World:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.cities = []
        self.scouts = []
        self.boats = []
        self.roads = []
        self.our_map = WorldMap(x, y)
        self.our_world_map = self.our_map.map_display_list()
        self.initial_seed_land = self.our_map.initial_seed_land
        self.land_objects = self.our_map.object_land
        self.initial_seed_land1 = [[" " for i in range(self.x)] for i in range(self.x)]
        self.initial_seed_water = self.our_map.initial_seed_water
        self.city_scatter(round(self.x/3))
        self.city_spawn()

    def print_state(self):
        city_number = len(self.cities)
        scout_number = len(self.scouts)
        road_number = len(self.roads)
        print("Cities: {}. Scouts: {}. Roads: {}.".format(city_number, scout_number, road_number))

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
        for i in self.boats:
            boat = i.get_location()
            world_map[boat[1]][boat[0]] = "B"
        for i in self.scout_path_list():
            x, y = i
            world_map[y][x] = "P"
        for i in self.roads:
            p_list = i.return_original_path()
            for i in p_list:
                world_map[i[1]][i[0]] = "R"
        for i in self.cities:
            j = i.get_location()
            world_map[j[1]][j[0]] = "C"
        return world_map
    #^shorten this function please

    def scout_path_list(self):
        self.meta_paths = []
        for i in self.scouts:
            slim_path = list(set(i.return_paths()))
            self.meta_paths.extend(slim_path)
        slimmed_meta = list(set(self.meta_paths))
        neatened = sorted(slimmed_meta)
        return neatened

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
                self.cities.append(City(possible_coordinate[0], possible_coordinate[1], possible_coordinate[0], possible_coordinate[1]))
                i += 1
            else:
                print("Done")
                i += 1

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

######OBJECT FUNCTIONS

    def get_object_from_location(self, coordinate_a, coordinate_b, type):
        for i in type:
            if i.x == coordinate_a and i.y == coordinate_b:
                return i

#####city functions

    def city_spawn_check(self):
        for i in self.cities:
            our_location = i.get_location()
            if i.growth > 0:
                i.add_growth()
            if i.growth > 10:
                print("Gotta do the spawn with city at {}!".format(our_location))
                self.spawn_function(i)
                i.growth = 0

    def proximity_check(self):
        for i in self.cities:
            i_loc = i.get_location()
            origin = i.return_city_origin()
            pos_cities = self.location_list(self.cities)
            potentials = self.neighbour_type_check_return(i_loc[0], i_loc[1], 2, pos_cities)
            for j in potentials:
                obj = self.return_object_from_location(self.cities, j[0], j[1])
                obj_origin = obj.return_city_origin()
                if origin != obj_origin:
                    print("Alert, city at {} with origin {} is near {} with origin {}".format(i_loc, origin, j, obj_origin))
                    dominant_origin = self.city_size_check(origin, obj_origin)
                    print("looks like cities with origin {} outnumber the others".format(dominant_origin))
                    if obj_origin != dominant_origin:
                        obj.x0 = dominant_origin[0]
                        obj.y0 = dominant_origin[1]
                    elif origin != dominant_origin:
                        i.x0 = dominant_origin[0]
                        i.y0 = dominant_origin[1]

    def city_size_check(self, origin_1, origin_2):
        orig_1_count = 0
        orig_2_count = 0
        for i in self.cities:
            orig = i.return_city_origin()
            if orig == origin_1:
                orig_1_count += 1
            if orig == origin_2:
                orig_2_count += 1
        print("{} count: {} /n {} count: {}".format(origin_1, orig_1_count, origin_2, orig_2_count))
        if orig_1_count > orig_2_count:
            return origin_1
        if orig_2_count > orig_1_count:
            return origin_2
        else:
            print("Equal")

    def city_block_check(self, origin_point):
        potential_neighbors = []
        for i in self.cities:
            if i.return_city_origin == origin_point:
                i_loc = i.get_location()
                potentials = self.neighbour_type_check_return(i_loc[0], i_loc[1], 1, self.location_list(self.cities))

    def city_origin_print(self):
        mega_list = []
        for i in self.cities:
            temp_list = []
            orig = i.return_city_origin()
            loc = i.get_location()
            temp_list.append(orig)
            temp_list.append(loc)
            mega_list.append(temp_list)
        mega_list_dict = {}
        for line in mega_list:
            if line[0] in mega_list_dict:
                mega_list_dict[line[0]].append(line[1])
            else:
                mega_list_dict[line[0]] = [line[1]]
        for k, v in mega_list_dict.items():
            print(k, v)

    def city_location_print(self):
        city_list = []
        for i in self.cities:
            loc = i.get_location()
            city_list.append(loc)
        city_list_sorted = sorted(city_list, key=lambda k: [k[0], k[1]])
        print("Cities...")
        print(city_list_sorted)


    #function to check if cities within 1 block of eachother have different origin. If so say "MERGING" and create super city.


#####SPAWN FUNCTIONS

    def city_spawn(self):
        for i in self.cities:
            self.spawn_function(i)
#            pos_water_points = self.neighbour_type_check_return(loc[0], loc[1], 1, self.initial_seed_water)
#            if len(pos_water_points) > 0:
#                our_boat = random.choice(pos_water_points)
#                self.boats.append(Scout(our_boat[0], our_boat[1], i.x0, i.y0))
#fix the boat thing

    def spawn_function(self, entity):
        loc = entity.get_location()
        pos_points = self.neighbour_type_check_return(loc[0], loc[1], 1, self.initial_seed_land)
        if loc in pos_points:
            pos_points.remove(loc)
        if len(pos_points) > 0:
            our_scout = random.choice(pos_points)
            self.scouts.append(Scout(our_scout[0], our_scout[1], entity.x0, entity.y0))
            print("SCOUT BORN AT {} {} with origin {} {}".format(our_scout[0], our_scout[1], entity.x0, entity.y0))



#####PROPAGATION FUNCTIONS
#function to look at city and check if part of a cluster
#if part of a cluster then create a shared origin point
#
#
    def check_origins(self, entity_class):
        for i in entity_class:
            our_loc = i.get_location()
            our_orig = i.return_city_origin()
            #print("City at {} has origin {}".format(our_loc, our_orig))


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
            scout_origin = i.x0, i.y0
            pos_cities = self.location_list(self.cities)
            pos_cities.remove(scout_origin)
            #print("Checking scout at: {} against cities: {}".format(i_loc, pos_cities))
            if i_loc not in pos_cities:
                self.scout_scanner(i, i_loc)

            potentials = self.neighbour_type_check_return(i_loc[0], i_loc[1], 3, pos_cities)
            #get city origins and remove ones with same origin as scout
            if len(potentials) > 0:
                self.city_distance_scanner(i, potentials)
            else:
                pos_moves = self.neighbour_type_check_return(i_loc[0], i_loc[1], 1, self.initial_seed_land)

                if len(pos_moves) > 0:
                    i.paths_taken.append(i_loc)
                    our_move = random.choice(pos_moves)
                    i.x = our_move[0]
                    i.y = our_move[1]

    def city_distance_scanner(self, scout_entity, possible_cities):
        our_city = random.choice(possible_cities)
        self.move_toward_city(scout_entity, our_city)

    def move_toward_city(self, original_entity, city_location):
        entity_location = original_entity.get_location()
        #print("generating potential paths between scout at {} with origin {} {} and city at: {}".format(entity_location, original_entity.x0, original_entity.y0, city_location))
        actual_distance_a = abs(entity_location[0] - city_location[0])
        actual_distance_b = abs(entity_location[1] - city_location[1])
        pos_moves = self.neighbour_type_check_return(entity_location[0], entity_location[1], 1, self.initial_seed_land)
        for i in pos_moves:
            move_distance_a = abs(i[0] - city_location[0])
            move_distance_b = abs(i[1] - city_location[1])
            if move_distance_a < actual_distance_a:
                original_entity.paths_taken.append(entity_location)
                original_entity.x = i[0]
            elif move_distance_b < actual_distance_b:
                original_entity.paths_taken.append(entity_location)
                original_entity.y = i[1]
            #else:
                #print("Got no candidates")
        #print("Scout location now: {} {}".format(original_entity.x, original_entity.y))


    def scout_scanner(self, scout, scout_location):
        #city_locations = self.location_list(self.cities)
        potential_collision = self.neighbour_type_check_return(scout_location[0], scout_location[1], 1, self.location_list(self.cities))
        origin = scout.x0, scout.y0
        print("Checking scout at: {} with origin {}".format(scout_location, origin))
        print("Our potential cities to link to: {}".format(potential_collision))
        if origin in potential_collision:
            potential_collision.remove(origin)
        for i in potential_collision:
            i_object = self.return_object_from_location(self.cities, i[0], i[1])
            i_origin = i_object.return_city_origin()
            if i_origin == origin:
                print("City at {} has origin {} so deleting".format(i, i_origin))
                potential_collision.remove(i)
                print("potential collision now: {}".format(potential_collision))
        if len(potential_collision) > 0:
            print("potential cities: {}".format(potential_collision))
            our_collision = random.choice(potential_collision)
            print("Our chosen city to attach to: {}".format(our_collision))
            potential_city = self.return_object_from_location(self.cities, our_collision[0], our_collision[1])
            potential_city_origin = potential_city.return_city_origin()
            self.cities.append((City(scout.x, scout.y, potential_city_origin[0], potential_city_origin[1])))
            our_new_city = self.return_object_from_location(self.cities, scout.x, scout.y)
            our_new_city.add_growth()
            #add growth to origin city
            origin_city = self.return_object_from_location(self.cities, scout.x0, scout.y0)
            origin_city.add_growth()
            our_paths = list(scout.return_paths())
            slimmed_path = list(set(our_paths))
            print("Scout paths: {}".format(our_paths))
            print("Slimmed scout paths: {}".format(slimmed_path))
            road_location = our_paths[-1]
            our_main_map = implementation.GridWithWeights(self.x, self.y)
            our_main_map_walls = self.initial_seed_land
            came_from, cost_so_far = implementation.dijkstra_search(our_main_map, (road_location[0], road_location[1]), (scout.x0, scout.y0))
            optimal_path = implementation.reconstruct_path(came_from, start=(road_location[0], road_location[1]), goal=(scout.x0, scout.y0))
            print(optimal_path)
            self.roads.append((Road(road_location[0], road_location[1], scout.x0, scout.y0, (scout.x, scout.y), optimal_path)))
            self.scouts.remove(scout)
            #do the city thing here



#####SMART ROUTE FUNCTIONS


####TRY TO IMPLEMENT A PATH_FINDER_FOR_ROAD
###GOAL, TAKE IN A POSITION AND A TARGET AND OUTPUT AN OPTIMAL PATH THAT RESPECTS WATER

    def smart_path_finder(self, our_location, our_desired_location):
        our_route = []
        print("Route finding against {} going to {}".format(our_location, our_desired_location))
        our_route.append(our_location)
        print("Routes: {}".format(our_route))







###TIMING STUFF WHICH WE NEED TO USE MORE

def test_function():
    L = [i for i in range(100)]

if __name__ == '__main__':
    t = Timer("test_function()", "from __main__ import test_function")
    print(t.timeit())