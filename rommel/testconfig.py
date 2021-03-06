from copy import deepcopy
import sys
import random
import os
import argparse
import Queue
from draw import draw_solution

# Import classes
execfile(os.getcwd() + '/assets/classes.py')


grid = Grid(12, 12)
grid.add_car(Car('hor', 2, 2, 5, red=True))
grid.add_car(Car('vert', 2, 0, 0))
grid.add_car(Car('vert', 3, 0, 3))
grid.add_car(Car('vert', 3, 1, 3))
grid.add_car(Car('vert', 2, 2, 8))
grid.add_car(Car('vert', 2, 3, 6))
grid.add_car(Car('vert', 2, 4, 5))
grid.add_car(Car('vert', 2, 5, 1))
grid.add_car(Car('vert', 2, 5, 3))
grid.add_car(Car('vert', 2, 5, 5))
grid.add_car(Car('vert', 2, 6, 0))
grid.add_car(Car('vert', 3, 6, 2))
grid.add_car(Car('vert', 3, 6, 6))
grid.add_car(Car('vert', 3, 6, 9))
grid.add_car(Car('vert', 2, 7, 6))
grid.add_car(Car('vert', 2, 9, 6))
grid.add_car(Car('vert', 2, 9, 10))
grid.add_car(Car('vert', 2, 10, 1))
grid.add_car(Car('vert', 3, 10, 9))
grid.add_car(Car('vert', 2, 11, 1))
grid.add_car(Car('vert', 2, 11, 8))
grid.add_car(Car('vert', 2, 11, 10))
grid.add_car(Car('hor', 3, 7, 0))
grid.add_car(Car('hor', 2, 10, 0))
grid.add_car(Car('hor', 3, 0, 2))
grid.add_car(Car('hor', 2, 3, 2))
grid.add_car(Car('hor', 2, 7, 2))
grid.add_car(Car('hor', 2, 7, 3))
grid.add_car(Car('hor', 2, 9, 3))
grid.add_car(Car('hor', 3, 2, 4))
grid.add_car(Car('hor', 3, 7, 4))
grid.add_car(Car('hor', 3, 0, 6))
grid.add_car(Car('hor', 2, 10, 6))
grid.add_car(Car('hor', 3, 0, 7))
grid.add_car(Car('hor', 2, 4, 7))
grid.add_car(Car('hor', 2, 10, 7))
grid.add_car(Car('hor', 2, 0, 8))
grid.add_car(Car('hor', 3, 3, 8))
grid.add_car(Car('hor', 3, 7, 8))
grid.add_car(Car('hor', 3, 3, 9))
grid.add_car(Car('hor', 2, 8, 9))
grid.add_car(Car('hor', 2, 1, 11))
grid.add_car(Car('hor', 3, 3, 11))
grid.add_car(Car('hor', 2, 7, 11))

print grid.grid


draw_solution([grid.grid])
  
