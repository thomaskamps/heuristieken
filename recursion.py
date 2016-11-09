from copy import deepcopy
import sys
import random
import os
import argparse

execfile(os.getcwd() + '/assets/classes.py')
sys.setrecursionlimit(150000000)

done_states = []

def recursive_brute_solver(grid):
    red_car = [x for x in grid.car_list[1:] if x.red][0]
    if red_car.start_x+red_car.length == len(grid.grid):
        return [grid.grid]
    
    temp_car_list = deepcopy(grid.car_list)
    random.shuffle(temp_car_list)
    for car in temp_car_list:
        if car != 'placeholder':
            car_n = grid.retrieve_value(car.start_x, car.start_y)
            if grid.check_move_car(car_n, 1):
                new_grid = deepcopy(grid)
                new_grid.move_car(car_n, 1)
                done_states.append(grid.grid)
                if new_grid.grid not in done_states:
                    temp = recursive_brute_solver(new_grid)
                    if temp:
                        return temp + [grid.grid]
                   
            if grid.check_move_car(car_n, -1):
                new_grid = deepcopy(grid)
                new_grid.move_car(car_n, -1)
                done_states.append(grid.grid)
                if new_grid.grid not in done_states:
                    temp = recursive_brute_solver(new_grid)
                    if temp:
                        return temp + [grid.grid]

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    
    parse.add_argument('--config', help='config to load', default=1, type=int)
    
    parse.add_argument('--print', dest='printer', action='store_true')
    parse.set_defaults(printer=False)

    parse.add_argument('--vis', dest='visual', action='store_true')
    parse.set_defaults(visual=False)

    args = parse.parse_args(sys.argv[1:])

    execfile(os.getcwd() + '/configs/' + str(args.config) + '.py')
    temp = recursive_brute_solver(grid)
    if args.printer:
        print(len(temp))
