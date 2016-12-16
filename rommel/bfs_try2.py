from copy import deepcopy
import sys
import random
import os
import argparse
import redis
import cPickle as pickle
from multiprocessing import Process
import time

# Import classes
execfile(os.getcwd() + '/assets/classes.py')

def bfs():
	"""
	Breadth First Search solver for the Rush Hour board game
	"""
	
	# Init vars etc.
	r = redis.StrictRedis(host='localhost', port=6379, db=0)
	re = redis.StrictRedis(host='localhost', port=6379, db=1)
	red = redis.StrictRedis(host='localhost', port=6379, db=2)
	
	# Main loop
	while True:
		# Take first grid from queue
		queue_item = re.lpop('queue')
		if not queue_item:
			break
		else:
			grid = pickle.loads(queue_item)
		
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
						if r.get(new_grid_str) != "1":
							
							# Check for solution (clear path to endpoint)
							if new_grid.check_solution():
								
								# Check if red car is at the endpoint
								if new_grid.car_list[1].start_x != (len(new_grid.grid[0])-2):
									
									# Add grid to queue to be further processed
									r.set(new_grid_str, "1")
									re.rpush('queue', pickle.dumps(new_grid))
									red.set(new_grid_str, str(grid.grid))
								
								# Return and finish algorithm
								else:
									red.set(new_grid_str, str(grid.grid))
									if red.get("finished") == "1":
										red.set('finished', str(new_grid.grid))
							
							# Add state to queue to be further processed
							r.set(new_grid_str, "1")
							re.rpush('queue', pickle.dumps(new_grid))
							red.set(new_grid_str, str(grid.grid))
				
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

    red = redis.StrictRedis(host='localhost', port=6379, db=2)
    red.flushall()
	
    re = redis.StrictRedis(host='localhost', port=6379, db=1)
    re.rpush('queue', pickle.dumps(grid))
	
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set(str(grid.grid), "1")
    red.set('finished', "1")
	
    processes = []
    processes.append(Process(target=bfs))
    processes[0].start()
    
    time.sleep(2)
    for x in range(1,6):
    	processes.append(Process(target=bfs))
    	processes[x].start()
    for pr in processes:
    	pr.join()
    
    while True:
    	time.sleep(0.1)
    	if red.get("finished") != "1":
    		for x in processes:
    			x.terminate()
    		state_list = []
    		state_list.append(eval(red.get("finished")))
    		current_grid = str(red.get("finished"))

    		while current_grid != str(grid.grid):
    			state_list.append(eval(red.get(current_grid)))
    			current_grid = red.get(current_grid)
    		break

    
    # If print is passed as argument, print number of moves
    if args.printer:
        print(len(state_list)-1)
		
	# If visual is passed as argument, draw visualisation
    if args.visual:
    	draw_solution(state_list)