
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

    def move_car(self, car_n, move):
        if self.check_move_car(car_n, move):
            car = self.car_list[car_n]
            
            if car.orientation == 'hor':
    
                if move == -1:
                    self.update_value(car.start_x+car.length-1, car.start_y, 0)
                    self.update_value(car.start_x-1, car.start_y, car_n)
                    
                elif move == 1:
                    self.update_value(car.start_x+car.length, car.start_y, car_n)
                    self.update_value(car.start_x, car.start_y, 0)
    
                self.car_list[car_n].start_x += move
    
            elif car.orientation == 'vert':
                
                if move == -1:
                    self.update_value(car.start_x, car.start_y+car.length-1, 0)
                    self.update_value(car.start_x, car.start_y-1, car_n)
            
                elif move == 1:
                    self.update_value(car.start_x, car.start_y+car.length, car_n)
                    self.update_value(car.start_x, car.start_y, 0)

                self.car_list[car_n].start_y += move

            return True

        else:
            return False

    def check_move_car(self, car_n, move):
        car = self.car_list[car_n]

        if car.orientation == 'hor':
            if move == -1:
                if car.start_x > 0:
                    if self.retrieve_value(car.start_x-1, car.start_y) == 0:
                        return True
            elif move == 1:
                if car.start_x + car.length < len(grid.grid[0]):
                    if self.retrieve_value(car.start_x+car.length, car.start_y) == 0:
                        return True

        elif car.orientation == 'vert':
            if move == -1:
                if car.start_y > 0:
                    if self.retrieve_value(car.start_x, car.start_y-1) == 0:
                        return True

            elif move == 1:
                if car.start_y + car.length < len(grid.grid):
                    if self.retrieve_value(car.start_x, car.start_y+car.length) == 0:
                        return True

        return False

    def check_solution(self):
        red_car = [x for x in self.car_list[1:] if x.red][0]
        if red_car.start_x+red_car.length == len(self.grid):
            return True
        no_path = False
        for i in range(red_car.start_x+red_car.length, len(self.grid)):
            if self.grid[red_car.start_y][i] != 0:
                no_path = True
                return False
        if no_path == False:
            return True
    

class Car(object):
    
    def __init__(self, orientation, length, start_x, start_y, red=False):
        self.orientation = orientation
        self.length = length
        self.start_x = start_x
        self.start_y = start_y
        self.red = red
