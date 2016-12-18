import Queue

class Solver(object):
	def __init__(self, grid, car_list):
		self.grid = grid
		self.car_list = car_list

	def a_star(self, grid, car_list):
		# Initialize variables
		queue, pre_grid = init_var_queue(grid, car_list, True)

		# Main loop
		while queue:
			
			# Take first grid from queue
			get_grid, gridObj = retrieve_grid(queue, True)
			
			# Check for all cars in the grid if there are moves possible
			for car in get_grid[2]:
			
				# Skip the placeholder car
				if car != 'placeholder':
				
					# Find the car number
					car_n = gridObj.retrieve_value(car[2], car[3])
					
					# Try to move selected car both ways
					returned = try_move(gridObj, car_n, get_grid, pre_grid, queue, "A", None)
					if returned:
						return returned

		return "No solution"

	def beam(self, grid, car_list):
		# Initialize variables
		beam = [(0, grid, car_list)]
		pre_grid = {}
		pre_grid[str(grid)] = "finished"
		width = 100
		solution = True

		while solution:

			queue = Queue.PriorityQueue()

			for x in beam:

				# Take first grid from queue
				get_grid = x
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
								
									# Heuristic: Distance red car to exit
									distancetoboard = len(newGridObj.grid) - newGridObj.car_list[1][2] - newGridObj.car_list[1][1]
									cost = distancetoboard + get_grid[0] 
									
									# Heuristic: Cost of blocking car is higher than blocking truck
									for i in range(newGridObj.car_list[1][2] + newGridObj.car_list[1][1], len(newGridObj.grid)):
										if newGridObj.retrieve_value(i, newGridObj.car_list[1][3]) != 0:
											if newGridObj.car_list[1][1] == 3:
												cost += 10
											if newGridObj.car_list[1][1] == 2:
												cost += 100
									
									# Check for solution (clear path to endpoint)
									if newGridObj.check_solution():
										
										# Check if red car is at the endpoint
										if newGridObj.car_list[1][2] != (len(newGridObj.grid[0])-2):
											
											# Add grid to queue to be further processed
											queue.put((cost, newGridObj.grid, newGridObj.car_list, get_grid[1][:]))
										
										# Return and finish algorithm
										else:
											pre_grid[newGridObjGridStr] = get_grid[1][:]
											return (newGridObj, pre_grid)
									
									# Add state to queue to be further processed
									queue.put((cost, newGridObj.grid, newGridObj.car_list, get_grid[1][:]))
						
						# Try to move selected car both ways
						returned = move_car(1)
						if returned:
							return returned
							
						returned = move_car(-1)
						if returned:
							return returned
			
			if queue.empty():
				print "Empty"
				return "No Solution"

			beam = []

			for i in range(width):
				if queue.empty():
					break
				else:
					obj = queue.get()
					beam.append(obj[:3])
					pre_grid[str(obj[1])] = obj[3]

			print len(pre_grid)

	def bfs(self, grid, car_list):
		queue, pre_grid = init_var_queue(grid, car_list, False)

		while queue:

			# Take first grid from queue
			get_grid, gridObj = retrieve_grid(queue, False)
			
			# Check for all cars in the grid if there are moves possible
			for car in get_grid[1]:
			
				# Skip the placeholder car
				if car != 'placeholder':
				
					# Find the car number
					car_n = gridObj.retrieve_value(car[2], car[3])
					
					# Try to move selected car both ways
					returned = try_move(gridObj, car_n, get_grid, pre_grid, queue, False, None)
					if returned:
						return returned

		return "No solution"

	def best_first(self, grid, car_list):
		queue, pre_grid = init_var_queue(grid, car_list, True)

		# Main loop
		while queue:
			
			# Take first grid from queue
			get_grid, gridObj = retrieve_grid(queue, True)
			
			# Check for all cars in the grid if there are moves possible
			for car in get_grid[2]:
			
				# Skip the placeholder car
				if car != 'placeholder':
				
					# Find the car number
					car_n = gridObj.retrieve_value(car[2], car[3])
					
					# Try to move selected car both ways
					returned = try_move(gridObj, car_n, get_grid, pre_grid, queue, "Best", None)
					if returned:
						return returned

		return "No solution"

# Init vars. etc
def init_var_queue(grid, car_list, heuristic):
	if heuristic == True:
		queue = Queue.PriorityQueue()
		queue.put((0, grid, car_list))
	else:
		queue = Queue.Queue()
		queue.put((grid, car_list))
	pre_grid = {}
	pre_grid[str(grid)] = "finished"
	return queue, pre_grid

def retrieve_grid(queue, heuristic):
	get_grid = queue.get()
	if heuristic == True:
		gridObj = Grid(get_grid[1], get_grid[2])
	else:
		gridObj = Grid(get_grid[0], get_grid[1])
	return get_grid, gridObj

# Function for moving the car, checking for solution and creating new states
def move_car(move, gridObj, car_n, get_grid, pre_grid, queue, heuristic, placeholder_pre_grid):
	if heuristic != False:
		num = 1
	else:
		num = 0
		cost = None
	
	# Check if move is possible
	if gridObj.check_move_car(car_n, move):
	
		# Create copy of grid and move the car in the new grid
		newGridObj = Grid([x[:] for x in get_grid[num]], get_grid[num+1][:])
		newGridObj.move_car(car_n, move)
		newGridObjGridStr = str(newGridObj.grid)
		
		# Check if grid has already existed
		if newGridObjGridStr not in pre_grid:

			if heuristic == "A":
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

			if heuristic == "Best":
				cost = len(newGridObj.grid) - newGridObj.car_list[1][2] - newGridObj.car_list[1][1]
				cost*= 5
				cost -= newGridObj.grid[newGridObj.car_list[1][3]].count(0)*10
			
			# Check for solution (clear path to endpoint)
			if newGridObj.check_solution():
				
				# Check if red car is at the endpoint
				if newGridObj.car_list[1][2] != (len(newGridObj.grid[0])-2):
					
					# Add grid to queue to be further processed
					if placeholder_pre_grid == None:
						queue, pre_grid = add_state(queue, cost, newGridObj, get_grid, pre_grid, newGridObjGridStr, num, heuristic)
					else:
						queue, placeholder_pre_grid = add_state(queue, cost, newGridObj, get_grid, placeholder_pre_grid, newGridObjGridStr, num, heuristic)
				
				# Return and finish algorithm
				else:
					pre_grid[newGridObjGridStr] = get_grid[num][:]
					return (newGridObj, pre_grid)
			
			# Add state to queue to be further processed
			if placeholder_pre_grid == None:
				queue, pre_grid = add_state(queue, cost, newGridObj, get_grid, pre_grid, newGridObjGridStr, num, heuristic)
			else:
				queue, placeholder_pre_grid = add_state(queue, cost, newGridObj, get_grid, placeholder_pre_grid, newGridObjGridStr, num, heuristic)

def add_state(queue, cost, newGridObj, get_grid, pre_grid, newGridObjGridStr, num, heuristic):
	if heuristic != False:
		queue.put((cost, newGridObj.grid, newGridObj.car_list))
	else:
		queue.put((newGridObj.grid, newGridObj.car_list))
	pre_grid[newGridObjGridStr] = get_grid[num][:]
	return queue, pre_grid

def try_move(gridObj, car_n, get_grid, pre_grid, queue, heuristic, placeholder_pre_grid):
	returned = move_car(1, gridObj, car_n, get_grid, pre_grid, queue, heuristic, placeholder_pre_grid)
	if returned:
		return returned
			
	returned = move_car(-1, gridObj, car_n, get_grid, pre_grid, queue, heuristic, placeholder_pre_grid)
	if returned:
		return returned