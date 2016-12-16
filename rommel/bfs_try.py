from copy import deepcopy
import sys
import random
import os
import argparse
from Queue import Queue
from draw import draw_solution
from multiprocessing import Process, Manager
import cPickle as pickle
import time
import redis

# Import classes
execfile(os.getcwd() + '/assets/classes.py')

def bfs():
	"""
	Breadth First Search solver for the Rush Hour board game
	"""
	r = redis.StrictRedis(host='localhost', port=6379, db=0)
	# Main loop
	while True:
		# Take first grid from queue
		grid = pickle.loads(r.lpop('queue'))
		
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
						new_grid_str = str(new_grid.grid)
						if r.get(new_grid_str) != "":
							
							# Check for solution (clear path to endpoint)
							if new_grid.check_solution():
								print "dsASAsaSAsaSasaS"
								
								# Check if red car is at the endpoint
								if new_grid.car_list[1].start_x != (len(new_grid.grid[0])-2):
									
									# Add grid to queue to be further processed
									r.set(new_grid_str, "")
									r.rpush('queue', pickle.dumps(new_grid))
								
								# Return and finish algorithm
								else:
									r.set(new_grid, grid)
									print "jeeeeejjjj"
									return (new_grid)
							
							# Add state to queue to be further processed
							r.set(new_grid_str, "")
							r.rpush('queue', pickle.dumps(new_grid))
				
				# Try to move selected car both ways
				move_car(1)
				move_car(-1)


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
    execfile(os.getcwd() + '/configs/' + str(args.config) + '.py')

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set(str(grid.grid), "")
    
    r.rpush('queue', pickle.dumps(grid))

    processes = []
    processes.append(Process(target=bfs))
    processes[0].start()
    
    time.sleep(4)
    for x in range(1,3):
    	processes.append(Process(target=bfs))
    	processes[x].start()
    for pr in processes:
    	pr.join()


	    
    # If print is passed as argument, print number of moves
    if args.printer:
        print(len(state_list)-1)
		
	# If visual is passed as argument, draw visualisation
    if args.visual:
    	draw_solution(state_list)