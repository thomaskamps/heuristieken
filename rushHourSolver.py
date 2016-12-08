import os
import argparse
import sys

# Import classes
execfile(os.getcwd() + '/assets/newClasses.py')
execfile(os.getcwd() + '/assets/solver.py')

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
    solver = Solver(grid.grid, grid.car_list)

    # Run algorithm and store return values
    temp = solver.aStar(grid.grid, grid.car_list)

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