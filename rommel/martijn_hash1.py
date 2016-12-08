from copy import deepcopy
import sys
import random
import os
import argparse
import Queue
import time
from draw import draw_solution

execfile(os.getcwd() + '/assets/classes.py')
sys.setrecursionlimit(150000000)

done_states = set([])

def hash(grid):
	numberList = []
	for row in grid:
		for element in row:
			numberList.append(element)
	number  = int(''.join(map(str,numberList)))
	
	return number

def bfsIter(grid):
	start_time = time.time()
	
	queue = Queue.Queue()

	queue.put(grid)

	done_states.add(hash(grid.grid))

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
					if hash(new_grid.grid) not in done_states:
						red_car = [x for x in grid.car_list[1:] if x.red][0]
						if new_grid.check_solution():
							if new_grid.car_list[1].start_x != (len(new_grid.grid[0])-2):
								done_states.add(hash(new_grid.grid))
								queue.put(new_grid)
								pre_grid[new_grid] = grid
							else:
								pre_grid[new_grid] = grid
								print("Time: %s seconds" % (time.time() - start_time))
								return (new_grid, pre_grid)
						done_states.add(hash(new_grid.grid))
						queue.put(new_grid)
						pre_grid[new_grid] = grid

				if grid.check_move_car(car_n, -1):
					new_grid = deepcopy(grid)
					new_grid.move_car(car_n, -1)
					if hash(new_grid.grid) not in done_states:
						red_car = [x for x in new_grid.car_list[1:] if x.red][0]
						if new_grid.check_solution():
							if new_grid.car_list[1].start_x != (len(new_grid.grid[0])-2):
								done_states.add(hash(new_grid.grid))
								queue.put(new_grid)
								pre_grid[new_grid] = grid
							else:
								pre_grid[new_grid] = grid
								print("Time: %s seconds" % (time.time() - start_time))
								return (new_grid, pre_grid)
						done_states.add(hash(new_grid.grid))
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

    if args.visual:
    	draw_solution(stateList)