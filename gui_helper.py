import os
import sys

# Import classes
execfile(os.getcwd() + '/assets/newClasses.py')
execfile(os.getcwd() + '/assets/solver.py')
#execfile(os.getcwd() + '/configsAlt/2.py')
	
def live_solver(algorithm, configuration):
	# Load selected config and construct grid
    execfile(os.getcwd() + '/configsAlt/' + str(configuration) + '.py', globals())
    solver = Solver(grid.grid, grid.car_list)

    # Run algorithm and store return values
    if algorithm == "bfs":
        temp = solver.bfs(grid.grid, grid.car_list)
    elif algorithm == "bestfirst":
        temp = solver.best_first(grid.grid, grid.car_list)
    elif algorithm == "astar":
        temp = solver.a_star(grid.grid, grid.car_list)

	# Construct statelist (shortest path)
    state_list = []
    state_list.append(temp[0].grid)
    current_grid = temp[0].grid
    print len(temp[1])

    while current_grid != grid.grid:
    	temper = temp[1][str(current_grid)]
    	state_list.append(temper)
    	current_grid = temper
    
    return [state_list[::-1], len(temp[1])]