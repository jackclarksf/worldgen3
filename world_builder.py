__author__ = 'iamja_000'

from itertools import product, starmap
import random
from timeit import Timer
from world_map import WorldMap
from entities import City, Scout, Road

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
            the_path = list(i.return_paths())
            slim_path = list(set(the_path))
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
            pos_cities = self.location_list(self.cities)
            scout_origin = i.x0, i.y0
            pos_cities.remove(scout_origin)
            #NEARBY CITY EVENT
            self.scout_scanner(i, i_loc)
            potentials = self.neighbour_type_check_return(i_loc[0], i_loc[1], 3, pos_cities)
            if len(potentials) > 0:
                print("We got some nearby cities, launching the event chain...")
                #self.city_distance_scanner(i, potentials)
                self.routefinding(scout_origin, potentials[0])
            else:
                print("NO nearby cities, standard movement")
                pos_moves = self.neighbour_type_check_return(i_loc[0], i_loc[1], 1, self.initial_seed_land)

                if len(pos_moves) > 0:
                    i.paths_taken.append(i_loc)
                    our_move = random.choice(pos_moves)
                    i.x = our_move[0]
                    i.y = our_move[1]

    def city_distance_scanner(self, scout_entity, possible_cities):
        for i in possible_cities:
            self.generate_potential_paths(scout_entity, i)

    def generate_potential_paths(self, original_entity, city_location):
        path_so_far = original_entity.return_paths()
        origination_point = original_entity.return_city_origin()
        print("generating potential paths between {} and city at: {}".format(origination_point, city_location))
        trimmed_path = list(set(path_so_far))
        print(trimmed_path)
        print(len(trimmed_path))
        #MEASURE DISTANCE BETWEEN ORIGINATION AND TARGET.
        distance_between_a = abs(origination_point[0] - city_location[0])
        distance_between_b = abs(origination_point[1] - city_location[1])
        print(distance_between_a, distance_between_b)
        start_point = list(origination_point)
        city_location_test = list(city_location)
        temp_list = []
        while start_point != city_location_test:
            print(start_point)
            pos_moves = self.neighbour_type_check_return(start_point[0], start_point[1], 1, self.initial_seed_land)
            if len(pos_moves) > 0:
                move_to_make = random.choice(pos_moves)
                start_point[0] = move_to_make[0]
                start_point[1] = move_to_make[1]
                temp_list.append(move_to_make)
        print(temp_list)
        print(len(temp_list))
        ####SO THIS IS GLORIOUSLY INEFFICIENT
        ####INSTEAD, WE SHOULD BUILD ROUTE_FINDING LOGIC FOR THE SCOUT, THEN USE THAT

#REIMPEMT THIS ALGORITHM https://www.raywenderlich.com/4946/introduction-to-a-pathfinding
    def routefinding(self, start_location, end_location):
        print("Checking between {} and {}".format(start_location, end_location))
        open_list = []
        closed_list = []
        closed_list.append(start_location)
        open_list.extend(self.neighbour_type_check_return(start_location[0], start_location[1], 1, self.initial_seed_land))
        open_list.remove(start_location)
        print(closed_list)
        print(open_list)

        def path_scoring_loop(path_to_score, start_location, end_location):
            list(start_location)
            list(path_to_score)
            test_route_dictionary = { }
            for i in path_to_score:
                actual_distance_a = abs(i[0] - start_location[0])
                actual_distance_b = abs(i[1] - start_location[1])
                combined_distance = actual_distance_a, actual_distance_b
                print("Distance: {}".format(combined_distance))
                #measure that punishes diagonals
                merged_distance = actual_distance_a + actual_distance_b
                print("Merged distance: {}".format(merged_distance))

                movement_distance = abs(start_location[0] - end_location[0]), abs(start_location[1] - end_location[1])
                merged_movement_distance =abs(start_location[0] - end_location[0]) + abs(start_location[1] - end_location[1])
                print(movement_distance)
                print(merged_movement_distance)
                our_final_score = merged_distance + merged_movement_distance
                print(our_final_score)
                test_route_dictionary[i] = our_final_score
            print(test_route_dictionary)

        while end_location not in open_list:
            test_route_dictionary = {}
            for i in open_list:
                actual_distance = abs(i[0] - start_location[0]), abs(i[1] - start_location[1])
                merged_distance = actual_distance[0] + actual_distance[1]
                movement_distance = abs(start_location[0] - end_location[0]), abs(start_location[1] - end_location[1])
                merged_movement_distance =abs(start_location[0] - end_location[0]) + abs(start_location[1] - end_location[1])
                our_final_score = merged_distance + merged_movement_distance
                print(our_final_score)
                test_route_dictionary[i] = our_final_score
            print(test_route_dictionary)



        path_scoring_loop(open_list, start_location, end_location)


    #IMPLEMENT THE A* ALGORITHM

    def scout_scanner(self, scout, scout_location):
        #GET CITY LOCATIONS
        city_locations = self.location_list(self.cities)
        potential_collision = self.neighbour_type_check_return(scout_location[0], scout_location[1], 1, city_locations)
        if len(potential_collision) > 0:
            collision_coordinate = potential_collision[0][0], potential_collision[0][1]
            potential_city = self.return_object_from_location(self.cities, collision_coordinate[0], collision_coordinate[1])
            orig_a, orig_b = potential_city.return_city_origin()
            print("Our potential city has origin: {} {}".format(orig_a, orig_b))
            origin = scout.x0, scout.y0
            print("Scout origin: {}".format(origin))
            if origin in potential_collision:
                potential_collision.remove(origin)
                print("Collisions now: {}".format(potential_collision))
                if len(potential_collision) > 0:
                    self.cities.append((City(scout.x, scout.y, collision_coordinate[0], collision_coordinate[1])))
                    our_paths = list(scout.return_paths())
                    slimmed_path = list(set(our_paths))
                    print("Scout paths: {}".format(slimmed_path))
                    road_location = our_paths[-1]

                    self.roads.append((Road(road_location[0], road_location[1], scout.x0, scout.y0, (scout.x, scout.y), our_paths)))
                    self.scouts.remove(scout)
            else:
                print("Looks like we are good to go!")
                self.cities.append((City(scout.x, scout.y, collision_coordinate[0], collision_coordinate[1])))
                our_paths = list(scout.return_paths())
                road_location = our_paths[-1]

                self.roads.append((Road(road_location[0], road_location[1], scout.x0, scout.y0, (scout.x, scout.y), our_paths)))
                self.scouts.remove(scout)



#####MOVEMENT FUNCTIONS








###TIMING STUFF WHICH WE NEED TO USE MORE

def test_function():
    L = [i for i in range(100)]

if __name__ == '__main__':
    t = Timer("test_function()", "from __main__ import test_function")
    print(t.timeit())