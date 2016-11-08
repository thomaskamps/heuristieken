from copy import deepcopy
import sys
import random
sys.setrecursionlimit(150000000)

done_states = []

class Grid(object):
    
    def __init__(self, length, width):
        self.grid = [[0 for i in range(width)] for j  in range(length)]
        self.car_list = ['placeholder']
    
    def retrieve_value(self, x, y):
        return self.grid[y][x]
    
    def update_value(self, x, y, value):
        self.grid[y][x] = value
        
    def add_car(self, car):
        index = len(self.car_list)
        self.car_list.append(car)
        
        for i in range(car.length):
            if car.orientation == 'vert':
                self.update_value(car.start_x, car.start_y+i, index)
            elif car.orientation == 'hor':
                self.update_value(car.start_x+i, car.start_y, index)

class Car(object):
    
    def __init__(self, orientation, length, start_x, start_y, red=False):
        self.orientation = orientation
        self.length = length
        self.start_x = start_x
        self.start_y = start_y
        self.red = red
        
        
grid = Grid(6, 6)
grid.add_car(Car('vert', 3, 2, 0))
grid.add_car(Car('vert', 3, 5, 0))
grid.add_car(Car('vert', 3, 3, 3))
grid.add_car(Car('vert', 2, 0, 4))
grid.add_car(Car('hor', 2, 1, 4))
grid.add_car(Car('hor', 2, 3, 0))
grid.add_car(Car('hor', 2, 3, 2, red=True))
grid.add_car(Car('hor', 2, 4, 3))
grid.add_car(Car('hor', 2, 4, 5))

def iterativeSolution(grid):
    valid_move = False
    solution = False
    pre_grid = {}
    while not solution:
        red_car = [x for x in grid.car_list[1:] if x.red][0]
        if red_car.start_x+red_car.length == len(grid.grid):
            print(len(pre_grid))
            return [grid.grid]
        no_path = False
        for i in range(red_car.start_x+red_car.length, len(grid.grid)):
            if grid.grid[red_car.start_y][i] != 0:
                no_path = True
                break
        if no_path == False:
            print("Path possible")
            print(len(pre_grid))
            return [grid.grid]
        temp_car_list = deepcopy(grid.car_list)
        random.shuffle(temp_car_list)
        for car in temp_car_list:
            if car != 'placeholder':
                if car.orientation == 'hor':
                    if car.start_x > 0:
                        if grid.retrieve_value(car.start_x-1, car.start_y) == 0:
                            new_grid = deepcopy(grid)
                            value = grid.retrieve_value(car.start_x, car.start_y)
                            new_grid.update_value(car.start_x+car.length-1, car.start_y, 0)
                            new_grid.update_value(car.start_x-1, car.start_y, value)
                            new_grid.car_list[value].start_x -= 1
                            done_states.append(grid.grid)
                            if new_grid.grid not in done_states:
                                valid_move = True
                                break
                            
                    if car.start_x + car.length < len(grid.grid[0]):
                        if grid.retrieve_value(car.start_x+car.length, car.start_y) == 0:
                            new_grid = deepcopy(grid)
                            value = grid.retrieve_value(car.start_x, car.start_y)
                            new_grid.update_value(car.start_x+car.length, car.start_y, value)
                            new_grid.update_value(car.start_x, car.start_y, 0)
                            new_grid.car_list[value].start_x += 1
                            if new_grid.grid not in done_states:
                                valid_move = True
                                break
                            
                elif car.orientation == 'vert':
                    if car.start_y > 0:
                        if grid.retrieve_value(car.start_x, car.start_y-1) == 0:
                            new_grid = deepcopy(grid)
                            value = grid.retrieve_value(car.start_x, car.start_y)
                            new_grid.update_value(car.start_x, car.start_y+car.length-1, 0)
                            new_grid.update_value(car.start_x, car.start_y-1, value)
                            new_grid.car_list[value].start_y -= 1
                            if new_grid.grid not in done_states:
                                valid_move = True
                                break
                            
                    if car.start_y + car.length < len(grid.grid):
                        if grid.retrieve_value(car.start_x, car.start_y+car.length) == 0:
                            new_grid = deepcopy(grid)
                            value = grid.retrieve_value(car.start_x, car.start_y)
                            new_grid.update_value(car.start_x, car.start_y+car.length, value)
                            new_grid.update_value(car.start_x, car.start_y, 0)
                            new_grid.car_list[value].start_y += 1
                            if new_grid.grid not in done_states:
                                valid_move = True
                                break

        if valid_move:
            pre_grid[new_grid] = grid
            grid = new_grid
            done_states.append(grid.grid)
            valid_move = False
        else:
            grid = pre_grid[grid]


temp = iterativeSolution(grid)
print(temp)
