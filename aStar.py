import Queue
from copy import deepcopy
import os
import argparse
import sys
from math import sqrt
from draw import draw_solution
import time

execfile(os.getcwd() + '/assets/classes.py')

done_states = []

def aStar(grid):

    # Init vars etc.
    done_states = []
    queue = Queue.PriorityQueue()
    queue.put((0, grid))
    done_states.insert(0,grid.grid)
    pre_grid = {}

    #Initiate queue
    while queue:

        #Retrieve the grid and the cost to get to that grid
        instance = queue.get()
        grid = instance[1]
        oldCost = instance[0]
        car_list = deepcopy(grid.car_list)

        #Loop through car list
        for car in car_list:

            #Check for placeholder which equals an empty space
            if car != "placeholder":

                #Define the current car and the red car
                car_n = grid.retrieve_value(car.start_x, car.start_y)
                red_car = [x for x in grid.car_list[1:] if x.red][0]

                #Checks if the car can move forward
                if grid.check_move_car(car_n, 1):
                    new_grid = deepcopy(grid)
                    new_grid.move_car(car_n, 1)

                    #Check whether the new state is already found
                    if new_grid.grid not in done_states:

                        red_car = [x for x in new_grid.car_list[1:] if x.red][0]
                        cost = 6 - red_car.start_x - red_car.length
                        for i in range(red_car.start_x + red_car.length, 6):
                            if new_grid.retrieve_value(i, red_car.start_y) != 0:
                                cost += 1

                        #Check whether the new grid is a solution
                        if new_grid.check_solution():
                            if new_grid.car_list[1].start_x != (len(new_grid.grid[0])-2):
                                done_states.insert(0, new_grid.grid)
                                queue.put((cost, new_grid))
                                pre_grid[new_grid] = grid
                            else:
                                #Returns the solution
                                pre_grid[new_grid] = grid
                                return (new_grid, pre_grid)

                        #If not a solution, add the new state to the queue and done states
                        done_states.insert(0, new_grid.grid)
                        queue.put((cost, new_grid))
                        pre_grid[new_grid] = grid

                #Checks whether the car can move backwards
                if grid.check_move_car(car_n, -1):
                    new_grid = deepcopy(grid)
                    new_grid.move_car(car_n, -1)

                    #Check whether the new board is a new state
                    if new_grid.grid not in done_states:

                        red_car = [x for x in new_grid.car_list[1:] if x.red][0]
                        cost = 6 - red_car.start_x - red_car.length
                        for i in range(red_car.start_x + red_car.length, 6):
                            if new_grid.retrieve_value(i, red_car.start_y) != 0:
                                cost += 1
                        
                        #Check for solution
                        if new_grid.check_solution():
                            if new_grid.car_list[1].start_x != (len(new_grid.grid[0])-2):
                                done_states.insert(0, new_grid.grid)
                                queue.put((cost, new_grid))
                                pre_grid[new_grid] = grid
                            else:
                                #Return solution
                                pre_grid[new_grid] = grid
                                return (new_grid, pre_grid)

                        #Add state to done states and put state in queue
                        done_states.insert(0, new_grid.grid)
                        queue.put((cost, new_grid))
                        pre_grid[new_grid] = grid

    return "No Solution"



if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    
    parse.add_argument('--config', help='config to load', default=1, type=int)
    
    parse.add_argument('--print', dest='printer', action='store_true')
    parse.set_defaults(printer=False)

    parse.add_argument('--vis', dest='visual', action='store_true')
    parse.set_defaults(visual=False)

    args = parse.parse_args(sys.argv[1:])

    execfile(os.getcwd() + '/configs/' + str(args.config) + '.py')
    start = time.clock()
    temp = aStar(grid)
    end = time.clock()
    print end-start
    if args.printer:
        print(temp[0].grid)

    finalGrid = temp[0]
    mothersGrids = temp[1]

    stateList = []
    stateList.append(finalGrid.grid)
    currentGrid = finalGrid

    while currentGrid.grid != grid.grid:
        stateList.append(mothersGrids[currentGrid].grid)
        currentGrid = mothersGrids[currentGrid]

    print(len(stateList)-1)

    if args.visual:
        draw_solution(stateList)