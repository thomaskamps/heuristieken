from copy import deepcopy
import sys
import random
import os
import argparse
from Queue import PriorityQueue
import redis
from multiprocessing import Process
import time
from multiprocessing.managers import SyncManager
import pickle

# Import classes
execfile(os.getcwd() + '/assets/newClasses.py')

def astar():
	"""
	Breadth First Search solver for the Rush Hour board game
	"""
	
	# Init vars etc.
	r = redis.StrictRedis(host='localhost', port=6379, db=0)
	re = redis.StrictRedis(host='localhost', port=6379, db=1)
	
	def pop():
		try:
			item = re.zrevrange('queue', 0, 0)[0]
			if re.zrem('queue', item) == 1:
				return item
			else:
				return pop()
		except IndexError:
			return None

	# Main loop
	while True:
		
		# Take first grid from queue
		get_grid = pop()
		if get_grid:
			get_grid = pickle.loads(get_grid)
			gridObj = Grid(get_grid[1], get_grid[2])
		else:
			break
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
						if not r.exists(newGridObjGridStr):
						
							cost = len(newGridObj.grid) - newGridObj.car_list[1][2] - newGridObj.car_list[1][1] + get_grid[0]
							for i in range(newGridObj.car_list[1][2] + newGridObj.car_list[1][1], len(newGridObj.grid)):
								if newGridObj.retrieve_value(i, newGridObj.car_list[1][3]) != 0:
									cost += 1
							cost = float(1)/cost * 10
							
							# Check for solution (clear path to endpoint)
							if newGridObj.check_solution():
								
								r.set(newGridObjGridStr, str(get_grid[1][:]))
								r.set("finished", str(newGridObj.grid))
							
							# Add state to queue to be further processed
							re.zincrby('queue', pickle.dumps((cost, newGridObj.grid, newGridObj.car_list)), cost)
							r.set(newGridObjGridStr, str(get_grid[1][:]))
				
				# Try to move selected car both ways
				move_car(1)	
				move_car(-1)


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
    
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    re = redis.StrictRedis(host='localhost', port=6379, db=1)
    r.flushall()
    r.set(str(grid), "finished")
    re.zincrby('queue', pickle.dumps((1, grid.grid, grid.car_list)), 1)
    
    processes = []
    processes.append(Process(target=astar))
    processes[0].start()
    
    time.sleep(2)
    for x in range(1,3):
    	processes.append(Process(target=astar))
    	processes[x].start()
    
    while True:
    	time.sleep(0.1)
    	if r.exists("finished"):
    		for x in processes:
    			x.terminate()
    		state_list = []
    		state_list.append(eval(r.get("finished")))
    		current_grid = r.get("finished")

    		while current_grid != str(grid.grid):
    			state_list.append(eval(r.get(current_grid)))
    			current_grid = r.get(current_grid)
    		break

    for pr in processes:
    	pr.join()

    # If print is passed as argument, print number of moves
    if args.printer:
        print(len(state_list)-1)
        print state_list
		
	# If visual is passed as argument, draw visualisation
    if args.visual:
    	draw_solution(state_list)