import Queue

class Solver(object):
	def __init__(self, grid, car_list):
		self.grid = grid
		self.car_list = car_list

	def a_star(self, grid, car_list, heur):
		heuristics = set(heur.split(','))

		# Initialize variables
		queue, pre_grid = init_var_queue(grid, car_list, heur)

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
					returned = try_move(gridObj, car_n, get_grid, pre_grid, queue, heuristics)
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
				get_grid, gridObj = retrieve_grid(x, "Beam")
				
				# Check for all cars in the grid if there are moves possible
				for car in get_grid[2]:
				
					# Skip the placeholder car
					if car != 'placeholder':
					
						# Find the car number
						car_n = gridObj.retrieve_value(car[2], car[3])
						
						# Try to move selected car both ways
						returned = try_move(gridObj, car_n, get_grid, pre_grid, queue, "Beam")
						if returned:
							return returned
			
			# Check if there are more grids to check
			if queue.empty():
				return "No Solution"

			beam = []

			# Fill up the beam with grids equal to the width
			queue, beam, pre_grid = fill_beam(width, queue, beam, pre_grid)

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
					returned = try_move(gridObj, car_n, get_grid, pre_grid, queue, False)
					if returned:
						return returned

		return "No solution"

	def dfs(self, grid, car_list):
		queue = Queue.LifoQueue()
		queue.put((grid, car_list))
		pre_grid = {}
		pre_grid[str(grid)] = "finished"

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
					returned = try_move(gridObj, car_n, get_grid, pre_grid, queue, False)
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
					returned = try_move(gridObj, car_n, get_grid, pre_grid, queue, "Best")
					if returned:
						return returned

		return "No solution"

# Init vars. etc
def init_var_queue(grid, car_list, heuristic):
	if heuristic != False:
		queue = Queue.PriorityQueue()
		queue.put((0, grid, car_list))
	else:
		queue = Queue.Queue()
		queue.put((grid, car_list))
	pre_grid = {}
	pre_grid[str(grid)] = "finished"
	return queue, pre_grid

# Set the grid object and retrieve the grid according to the algorithm
def retrieve_grid(queue, heuristic):
	if heuristic == "Beam":
		get_grid = queue
	else:
		get_grid = queue.get()
	if heuristic != False:
		gridObj = Grid(get_grid[1], get_grid[2])
	else:
		gridObj = Grid(get_grid[0], get_grid[1])
	return get_grid, gridObj

# Function for moving the car, checking for solution and creating new states
def move_car(move, gridObj, car_n, get_grid, pre_grid, queue, heuristic):
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

			if heuristic != False:
				if heuristic != "Best":

					# Add the cost of the previous board
					cost = get_grid[0]

				if "1" in heuristic or heuristic == "Beam":

					# Heuristic: Distance red car to exit
					cost = red_to_end(newGridObj) + cost

				if "2" in heuristic:

					# Heuristic: More cars in fron of the red car is higher cost
					for i in range(newGridObj.car_list[1][2] + newGridObj.car_list[1][1], len(newGridObj.grid)):
						if newGridObj.retrieve_value(i, newGridObj.car_list[1][3]) != 0:
							cost += 1000

				if "3" in heuristic or heuristic == "Beam": 
					
					# Heuristic: Cost of blocking car is higher than blocking truck
					for i in range(newGridObj.car_list[1][2] + newGridObj.car_list[1][1], len(newGridObj.grid)):
						if newGridObj.retrieve_value(i, newGridObj.car_list[1][3]) != 0:
							if newGridObj.car_list[1][1] == 3:
								cost += 1000
							if newGridObj.car_list[1][1] == 2:
								cost += 100

				if "4" in heuristic:

					# Heuristic: Add cost if more cars are blocked by other cars
					# Loop through the car list
					for car in newGridObj.car_list:
						if car != 'placeholder':

							car_num = newGridObj.retrieve_value(car[2], car[3])
							
							# Adds cost if a car is blocked by another car, higher cost for cars above or behind
							if newGridObj.check_move_car(car_num, 1):
								cost += 10

							if newGridObj.check_move_car(car_num, -1):
								cost += 100

				if heuristic == "Best":
					cost = red_to_end(newGridObj)
					cost*= 5
					cost -= newGridObj.grid[newGridObj.car_list[1][3]].count(0)*10
			
			# Check for solution (clear path to endpoint)
			if newGridObj.check_solution():
				
				# Check if red car is at the endpoint
				if newGridObj.car_list[1][2] != (len(newGridObj.grid[0])-2):
					
					# Add grid to queue to be further processed
					queue, pre_grid = add_state(queue, cost, newGridObj, get_grid, pre_grid, newGridObjGridStr, num, heuristic)
				
				# Return and finish algorithm
				else:
					pre_grid[newGridObjGridStr] = get_grid[num][:]
					return (newGridObj, pre_grid)
			
			# Add state to queue to be further processed
			queue, pre_grid = add_state(queue, cost, newGridObj, get_grid, pre_grid, newGridObjGridStr, num, heuristic)

# Heuristic: Distance from the red car to the end
def red_to_end(newGridObj):
	return len(newGridObj.grid) - newGridObj.car_list[1][2] - newGridObj.car_list[1][1]

#Fill the queue according to the algorithm
def add_state(queue, cost, newGridObj, get_grid, pre_grid, newGridObjGridStr, num, heuristic):
	if heuristic != False:
		if heuristic == "Beam":
			queue.put((cost, newGridObj.grid, newGridObj.car_list, get_grid[num][:]))
		else:
			queue.put((cost, newGridObj.grid, newGridObj.car_list))
	else:
		queue.put((newGridObj.grid, newGridObj.car_list))

	# Add to pre_grid
	if heuristic != "Beam":
		pre_grid[newGridObjGridStr] = get_grid[num][:]
	return queue, pre_grid

# Try to move a car both ways
def try_move(gridObj, car_n, get_grid, pre_grid, queue, heuristic):
	returned = move_car(1, gridObj, car_n, get_grid, pre_grid, queue, heuristic)
	if returned:
		return returned
			
	returned = move_car(-1, gridObj, car_n, get_grid, pre_grid, queue, heuristic)
	if returned:
		return returned

# Fill the beam according to the given width
def fill_beam(width, queue, beam, pre_grid):
	for i in range(width):
		if queue.empty():
			break
		else:
			obj = queue.get()
			beam.append(obj[:3])
			pre_grid[str(obj[1])] = obj[3]

	return queue, beam, pre_grid
