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
	queue = Queue.Queue()

	queue.put(grid)

	done_states.append(grid.grid)

	pre_grid = {}

	while queue:
		grid = queue.get()
		car_list = deepcopy(grid.car_list)
		for car in car_list:
			if car != 'placeholder':
				car_n = grid.retrieve_value(car.start_x, car.start_y)
				
				if grid.check_move_car(car_n, 1):
					new_grid = deepcopy(grid)
					new_grid.move_car(car_n, 1)
					if new_grid.grid not in done_states:
						red_car = [x for x in grid.car_list[1:] if x.red][0]
						if red_car.start_x+red_car.length == len(grid.grid):
							pre_grid[new_grid] = grid
							return (new_grid, pre_grid)
						done_states.append(new_grid.grid)
						queue.put(new_grid)
						pre_grid[new_grid] = grid

				if grid.check_move_car(car_n, -1):
					new_grid = deepcopy(grid)
					new_grid.move_car(car_n, -1)
					if new_grid.grid not in done_states:
						red_car = [x for x in new_grid.car_list[1:] if x.red][0]
						if red_car.start_x+red_car.length == len(grid.grid):
							pre_grid[new_grid] = grid
							return (new_grid, pre_grid)
						done_states.append(new_grid.grid)
						queue.put(new_grid)
						pre_grid[new_grid] = grid

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
        print(temp[0].grid)

    finalGrid = temp[0]
    mothersGrids = temp[1]

    stateList = []
    stateList.append(finalGrid.grid)
    currentGrid = finalGrid

    while currentGrid.grid != grid.grid:
    	stateList.append(mothersGrids[currentGrid].grid)
    	currentGrid = mothersGrids[currentGrid]

    print(len(stateList))