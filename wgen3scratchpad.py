__author__ = 'iamja_000'

from itertools import product, starmap

x = 20
y = 20

def world_coordinates():
    w_coord = list(product(range(x), range(y)))
    return w_coord

our_coord = world_coordinates()
print(our_coord)

def border_adder(base_coord_list):
    the_new_borders = []
    for i in base_coord_list:
        a, b, = i
        if a == 0:
            the_new_borders.append(i)
        elif b == 0:
            the_new_borders.append(i)
        elif a == x-1:
            the_new_borders.append(i)
        elif b == y-1:
            the_new_borders.append(i)
    return the_new_borders

our_borders = border_adder(our_coord)
print("TEST")
print(our_borders)

