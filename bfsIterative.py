from copy import deepcopy
import sys
import random
import os
import argparse
import Queue

execfile(os.getcwd() + '/assets/classes.py')
sys.setrecursionlimit(150000000)

done_states = []

def bfsIter(grid):
	car_list = deepcopy(grid.car_list)
	queue = Queue.Queue()

	queue.put(grid)

	done_states.append(grid)

	while queue:
		grid = queue.get()
		for car in car_list:
			if car != "placeholder":
				car_n = grid.retrieve_value(car.start_x, car.start_y)

				if grid.check_move_car(car_n, 1):
					new_grid = deepcopy(grid)
					new_grid.move_car(car_n, 1)
					if new_grid not in done_states:
						done_states.append(new_grid)
						queue.put(new_grid)

				if grid.check_move_car(car_n, -1):
					new_grid = deepcopy(grid)
					new_grid.move_car(car_n, -1)
					if new_grid not in done_states:
						done_states.append(new_grid)
						queue.put(new_grid)

	return "No solution"

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    
    parse.add_argument('--config', help='config to load', default=1, type=int)
    
    parse.add_argument('--print', dest='printer', action='store_true')
    parse.set_defaults(printer=False)

    parse.add_argument('--vis', dest='visual', action='store_true')
    parse.set_defaults(visual=False)

    args = parse.parse_args(sys.argv[1:])

    execfile(os.getcwd() + '/configs/' + str(args.config) + '.py')
    temp = bfsIter(grid)
    if args.printer:
        print(len(temp))