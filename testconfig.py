from copy import deepcopy
import sys
import random
import os
import argparse
import Queue
from draw import draw_solution

# Import classes
execfile(os.getcwd() + '/assets/classes.py')


grid = Grid(9, 9)
grid.add_car(Car('hor', 2, 1, 4, red=True))
grid.add_car(Car('vert', 2, 0, 0))
grid.add_car(Car('vert', 2, 0, 4))
grid.add_car(Car('vert', 2, 0, 7))
grid.add_car(Car('vert', 3, 2, 5))
grid.add_car(Car('vert', 3, 3, 1))
grid.add_car(Car('vert', 2, 3, 4))
grid.add_car(Car('vert', 2, 3, 6))
grid.add_car(Car('vert', 2, 4, 7))
grid.add_car(Car('vert', 3, 5, 0))
grid.add_car(Car('vert', 3, 8, 2))
grid.add_car(Car('vert', 3, 8, 5))
grid.add_car(Car('hor', 2, 0, 3))
grid.add_car(Car('hor', 2, 0, 6))
grid.add_car(Car('hor', 3, 1, 8))
grid.add_car(Car('hor', 3, 1, 0))
grid.add_car(Car('hor', 2, 4, 6))
grid.add_car(Car('hor', 3, 5, 3))
grid.add_car(Car('hor', 3, 5, 5))
grid.add_car(Car('hor', 2, 5, 8))
grid.add_car(Car('hor', 3, 6, 1))
grid.add_car(Car('hor', 2, 7, 8))

print grid.grid


draw_solution([grid.grid])
  
