from copy import deepcopy
import sys
import random
import os
import argparse
import Queue
from draw import draw_solution
import itertools

# Import classes
execfile(os.getcwd() + '/assets/newClasses.py')
	
def id_dfs(grid, car_list):

	def get_moves(get_grid, gridObj):
		returner = []
		
		for car in get_grid[2]:
		
			# Skip the placeholder car
			if car != 'placeholder':
			
				# Find the car number
				car_n = gridObj.retrieve_value(car[2], car[3])
				
				# Function for moving the car, checking for solution and creating new states
				def move_car(move):
					
					# Check if move is possible
					if gridObj.check_move_car(car_n, move):
					
						# Create copy of grid and move the car in the new grid
						newGridObj = Grid([x[:] for x in get_grid[1]], get_grid[2][:])
						newGridObj.move_car(car_n, move)
						
						cost = len(newGridObj.grid) - newGridObj.car_list[1][2] - newGridObj.car_list[1][1]
						cost*= 5
						cost -= newGridObj.grid[newGridObj.car_list[1][3]].count(0)*10
						
						# Add state to queue to be further processed
						returner.append((cost, newGridObj.grid, newGridObj.car_list))
			
				# Try to move selected car both ways
				move_car(1)
				move_car(-1)
		return returner

	def dfs(route, depth):
		if depth == 0:
			return

		get_grid = route[-1]
		gridObj = Grid(get_grid[1], get_grid[2])

		if gridObj.check_solution():
			return route
		
		moves = get_moves(get_grid, gridObj)
		moves.sort()
		moves = moves[:3]
		for move in moves:
			if move not in route:
				next_route = dfs(route + [move], depth - 1)
				if next_route:
					return next_route

	for depth in itertools.count():
		print depth
		route = dfs([(1, grid, car_list)], 32)
		if route:
			return route


# Initializer (loads settings etc.)
if __name__ == '__main__':
	parse = argparse.ArgumentParser()

	# Choose which config to load
	parse.add_argument('--config', help='config to load', default=1, type=int)

	# Choose if the number of moves should be printed
	parse.add_argument('--print', dest='printer', action='store_true')
	parse.set_defaults(printer=False)
		
	# Choose if a visualisation should be made
	parse.add_argument('--visual', dest='visual', action='store_true')
	parse.set_defaults(visual=False)

	args = parse.parse_args(sys.argv[1:])
	
	# Load selected config and construct grid
	execfile(os.getcwd() + '/configsAlt/' + str(args.config) + '.py')

	# Run algorithm and store return values
	temp = id_dfs(grid.grid, grid.car_list)

	print len(temp)
	print temp
