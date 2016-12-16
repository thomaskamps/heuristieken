from copy import deepcopy
import sys
import random
import os
import argparse
import Queue
from draw import draw_solution
import time

# Import classes
execfile(os.getcwd() + '/assets/classes.py')

def bfs(grid):
	"""
	Breadth First Search solver for the Rush Hour board game
	"""
	
	# Init vars etc.
	done_states = []
	queue = Queue.Queue()
	queue.put(grid)
	done_states.insert(0,grid.grid)
	pre_grid = {}

	# Main loop
	while queue:
		
		# Take first grid from queue
		grid = queue.get()
		
		# Check for all carss in the grid if there are moves possible
		for car in grid.car_list:
		
			# Skip the placeholder car
			if car != 'placeholder':
			
				# Find the car number
				car_n = grid.retrieve_value(car.start_x, car.start_y)
				
				# Function for moving the car, checking for solution and creating new states
				def move_car(move):
					
					# Check if move is possible
					if grid.check_move_car(car_n, move):
					
						# Create copy of grid and move the car in the new grid
						new_grid = deepcopy(grid)
						new_grid.move_car(car_n, move)
						
						# Check if grid has already existed
						if new_grid.grid not in done_states:
							
							# Check for solution (clear path to endpoint)
							if new_grid.check_solution():
								
								# Check if red car is at the endpoint
								if new_grid.car_list[1].start_x != (len(new_grid.grid[0])-2):
									
									# Add grid to queue to be further processed
									done_states.insert(0, new_grid.grid)
									queue.put(new_grid)
									pre_grid[new_grid] = grid
								
								# Return and finish algorithm
								else:
									pre_grid[new_grid] = grid
									return (new_grid, pre_grid)
							
							# Add state to queue to be further processed
							done_states.insert(0, new_grid.grid)
							queue.put(new_grid)
							pre_grid[new_grid] = grid
				
				# Try to move selected car both ways
				returned = move_car(1)
				if returned:
					return returned
					
				returned = move_car(-1)
				if returned:
					return returned

	return "No solution"


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

    parse.add_argument('--time', dest='time', action='store_true')
    parse.set_defaults(time=False)

    args = parse.parse_args(sys.argv[1:])
	
	# Load selected config and construct grid
    execfile(os.getcwd() + '/configs/' + str(args.config) + '.py')

    if args.time:
    	start = time.clock()
    
    # Run algorithm and store return values
    temp = bfs(grid)

    if args.time:
    	end = time.clock()
    	print end - start

	# Construct statelist (shortest path)
    state_list = []
    state_list.append(temp[0].grid)
    current_grid = temp[0]
    print len(temp[1])

    while current_grid.grid != grid.grid:
    	state_list.append(temp[1][current_grid].grid)
    	current_grid = temp[1][current_grid]
    
    # If print is passed as argument, print number of moves
    if args.printer:
        print(len(state_list)-1)
		
	# If visual is passed as argument, draw visualisation
    if args.visual:
    	draw_solution(state_list)