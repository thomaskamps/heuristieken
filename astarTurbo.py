from copy import deepcopy
import sys
import random
import os
import argparse
import Queue
from draw import draw_solution

# Import classes
execfile(os.getcwd() + '/assets/newClasses.py')

def bfs(grid, car_list):
	"""
	Breadth First Search solver for the Rush Hour board game
	"""
	
	# Init vars etc.
	queue = Queue.PriorityQueue()
	queue.put((0, grid, car_list))
	pre_grid = {}
	pre_grid[str(grid)] = "finished"

	# Main loop
	while queue:
		
		# Take first grid from queue
		get_grid = queue.get()
		gridObj = Grid(get_grid[1], get_grid[2])
		
		# Check for all cars in the grid if there are moves possible
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
						newGridObjGridStr = str(newGridObj.grid)
						
						# Check if grid has already existed
						if newGridObjGridStr not in pre_grid:
						
							cost = 6 - newGridObj.car_list[1][2] - newGridObj.car_list[1][1]
							for i in range(newGridObj.car_list[1][2] + newGridObj.car_list[1][1], 6):
								if newGridObj.retrieve_value(i, newGridObj.car_list[1][3]) != 0:
									cost += 1
							
							# Check for solution (clear path to endpoint)
							if newGridObj.check_solution():
								
								# Check if red car is at the endpoint
								if newGridObj.car_list[1][2] != (len(newGridObj.grid[0])-2):
									
									# Add grid to queue to be further processed
									queue.put((cost, newGridObj.grid, newGridObj.car_list))
									pre_grid[newGridObjGridStr] = get_grid[1][:]
								
								# Return and finish algorithm
								else:
									pre_grid[newGridObjGridStr] = get_grid[1][:]
									return (newGridObj, pre_grid)
							
							# Add state to queue to be further processed
							queue.put((cost, newGridObj.grid, newGridObj.car_list))
							pre_grid[newGridObjGridStr] = get_grid[1][:]
				
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

    args = parse.parse_args(sys.argv[1:])
	
	# Load selected config and construct grid
    execfile(os.getcwd() + '/configsAlt/' + str(args.config) + '.py')

    # Run algorithm and store return values
    temp = bfs(grid.grid, grid.car_list)

	# Construct statelist (shortest path)
    state_list = []
    state_list.append(temp[0].grid)
    current_grid = temp[0].grid
    print len(temp[1])

    while current_grid != grid.grid:
    	temper = temp[1][str(current_grid)]
    	state_list.append(temper)
    	current_grid = temper
    
    # If print is passed as argument, print number of moves
    if args.printer:
        print(len(state_list)-1)
		
	# If visual is passed as argument, draw visualisation
    if args.visual:
    	draw_solution(state_list)