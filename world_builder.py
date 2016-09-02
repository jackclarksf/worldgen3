__author__ = 'iamja_000'

from itertools import product, starmap
import random
from timeit import Timer
from world_map import WorldMap
from entities import City, Scout, Road
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
        self.initial_seed_land1 = [[" " for i in range(self.x)] for i in range(self.x)]
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
        for i in self.boats:
            boat = i.get_location()
            world_map[boat[1]][boat[0]] = "B"
        path_list = self.scout_path_list()
        for i in path_list:
            x, y = i
            world_map[y][x] = "P"
        for i in self.roads:
            p_list = i.return_original_path()
            for i in p_list:
                x, y = i
                world_map[y][x] = "R"
        for i in self.cities:
            j = i.get_location()
            world_map[j[1]][j[0]] = "C"
        return world_map

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
                print("Pos coordinate chosen = {}".format(possible_coordinate))
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

#####SPAWN FUNCTIONS

    def city_spawn(self):
        for i in self.cities:
            loc = i.get_location()
            pos_points = self.neighbour_type_check_return(loc[0], loc[1], 1, self.initial_seed_land)
            pos_points.remove(loc)
            if len(pos_points) > 0:
                our_scout = random.choice(pos_points)
                self.scouts.append(Scout(our_scout[0], our_scout[1], i.x0, i.y0))
                pos_water_points = self.neighbour_type_check_return(loc[0], loc[1], 1, self.initial_seed_water)
            if len(pos_water_points) > 0:
                our_boat = random.choice(pos_water_points)
                self.boats.append(Scout(our_boat[0], our_boat[1], i.x0, i.y0))


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
        print("generating potential paths between scout at {} with origin {} {} and city at: {}".format(entity_location, original_entity.x0, original_entity.y0, city_location))
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
            else:
                print("Got no candidates")
        print("Scout location now: {} {}".format(original_entity.x, original_entity.y))

#REIMPEMT THIS ALGORITHM https://www.raywenderlich.com/4946/introduction-to-a-pathfinding
    def routefinding(self, start_location, end_location):
        print("Checking between {} and {}".format(start_location, end_location))
        tuckaway = start_location
        open_list = []
        closed_list = []
        closed_list.append(start_location)

        while end_location not in closed_list:
            test_route_dictionary = {}
            print("Testing location: {}".format(start_location))
            open_list.extend(self.neighbour_type_check_return(start_location[0], start_location[1], 1, self.initial_seed_land))
            open_list.remove(start_location)
            open_list = list(set(open_list))
            print("Open list is: {}".format(open_list))
            for i in open_list:
                if i in closed_list:
                    continue
                else:
                    merged_distance = abs(i[0] - start_location[0]) + abs(i[1] - start_location[1])
                    merged_movement_distance = abs(start_location[0] - end_location[0]) + abs(start_location[1] - end_location[1])
                    our_final_score = merged_distance + merged_movement_distance
                    test_route_dictionary[i] = our_final_score
            print("Test route dictionary is: {}".format(test_route_dictionary))
            min_val = min(test_route_dictionary.values())
            pos_values = [k for k, v in test_route_dictionary.items() if v == min_val]
            print("Low val options: {}".format(pos_values))
            potential_route = random.choice(pos_values)
            print("Chosen option: {}".format(potential_route))
            closed_list.append(potential_route)
            open_list.remove(potential_route)
            if start_location in test_route_dictionary:
                del test_route_dictionary[start_location]
            start_location = potential_route
        print("Checked between {} and {} \n route: {}".format(tuckaway, end_location, closed_list))


    #IMPLEMENT THE A* ALGORITHM

    def scout_scanner(self, scout, scout_location):
        city_locations = self.location_list(self.cities)
        potential_collision = self.neighbour_type_check_return(scout_location[0], scout_location[1], 1, city_locations)
        origin = scout.x0, scout.y0
        if origin in potential_collision:
            potential_collision.remove(origin)
        if len(potential_collision) > 0:
            our_collision = random.choice(potential_collision)
            potential_city = self.return_object_from_location(self.cities, our_collision[0], our_collision[1])
            orig_a, orig_b = potential_city.return_city_origin()
            self.cities.append((City(scout.x, scout.y, our_collision[0], our_collision[1])))
            our_paths = list(scout.return_paths())
            slimmed_path = list(set(our_paths))
            print("Scout paths: {}".format(our_paths))
            print("Slimmed scout paths: {}".format(slimmed_path))
            road_location = our_paths[-1]
            self.smart_path_finder((scout.x0, scout.y0), (scout_location[0], scout_location[1]))
            our_main_map = implementation.GridWithWeights(self.x, self.y)
            our_main_map_walls = self.initial_seed_land
            came_from, cost_so_far = implementation.dijkstra_search(our_main_map, (road_location[0], road_location[1]), (scout.x0, scout.y0))
            print("Standard paths: {}".format(our_paths))
            print("New paths: {}".format(implementation.reconstruct_path(came_from, start=(road_location[0], road_location[1]), goal=(scout.x0, scout.y0))))
            optimal_path = implementation.reconstruct_path(came_from, start=(road_location[0], road_location[1]), goal=(scout.x0, scout.y0))
            print(optimal_path)
            self.roads.append((Road(road_location[0], road_location[1], scout.x0, scout.y0, (scout.x, scout.y), optimal_path)))
            self.scouts.remove(scout)



#####SMART ROUTE FUNCTIONS


####TRY TO IMPLEMENT A PATH_FINDER_FOR_ROAD
###GOAL, TAKE IN A POSITION AND A TARGET AND OUTPUT AN OPTIMAL PATH THAT RESPECTS WATER

    def smart_path_finder(self, our_location, our_desired_location):
        our_route = []
        print("Route finding against {} going to {}".format(our_location, our_desired_location))
        our_route.append(our_location)
        print("Routes: {}".format(our_route))



#something pretty screw happening here






###TIMING STUFF WHICH WE NEED TO USE MORE

def test_function():
    L = [i for i in range(100)]

if __name__ == '__main__':
    t = Timer("test_function()", "from __main__ import test_function")
    print(t.timeit())