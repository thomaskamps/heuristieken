from copy import deepcopy
import sys
import random
import os
import argparse
import Queue
from draw import draw_solution

class Solver(object):
	def __init__(self, grid, car_list):
		self.grid = grid
		self.car_list = car_list

	def aStar(self, grid, car_list):

		# Initialize variables
		queue, pre_grid = init_var(grid, car_list)

		# Main loop
		while queue:
			
			# Take first grid from queue
			get_grid, gridObj = retrieve_grid(queue)
			
			# Check for all cars in the grid if there are moves possible
			for car in get_grid[2]:
			
				# Skip the placeholder car
				if car != 'placeholder':
				
					# Find the car number
					car_n = gridObj.retrieve_value(car[2], car[3])
					
					# Try to move selected car both ways
					returned = move_car(1, gridObj, car_n, get_grid, pre_grid, queue)
					if returned:
						return returned
						
					returned = move_car(-1, gridObj, car_n, get_grid, pre_grid, queue)
					if returned:
						return returned

		return "No solution"

# Init vars. etc
def init_var(grid, car_list):
	queue = Queue.PriorityQueue()
	queue.put((0, grid, car_list))
	pre_grid = {}
	pre_grid[str(grid)] = "finished"
	return queue, pre_grid

def retrieve_grid(queue):
	get_grid = queue.get()
	gridObj = Grid(get_grid[1], get_grid[2])
	return get_grid, gridObj

# Function for moving the car, checking for solution and creating new states
def move_car(move, gridObj, car_n, get_grid, pre_grid, queue):
	
	# Check if move is possible
	if gridObj.check_move_car(car_n, move):
	
		# Create copy of grid and move the car in the new grid
		newGridObj = Grid([x[:] for x in get_grid[1]], get_grid[2][:])
		newGridObj.move_car(car_n, move)
		newGridObjGridStr = str(newGridObj.grid)
		
		# Check if grid has already existed
		if newGridObjGridStr not in pre_grid:
		
			# Heuristic: Distance red car to exit
			distancetoboard = len(newGridObj.grid) - newGridObj.car_list[1][2] - newGridObj.car_list[1][1]
			cost =  distancetoboard + get_grid[0] 
			
			# Heuristic: Cost of blocking car is higher than blocking truck
			for i in range(newGridObj.car_list[1][2] + newGridObj.car_list[1][1], len(newGridObj.grid)):
				if newGridObj.retrieve_value(i, newGridObj.car_list[1][3]) != 0:
					if newGridObj.car_list[1][1] == 3:
						cost += 10
					if newGridObj.car_list[1][1] == 2:
						cost += 1000
			
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