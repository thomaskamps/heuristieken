
class Grid(object):
    """
    Class used to solve the Rush Hour boardgame.
    Initializes a playing board, and can perform several operations on it.
    """
    
    def __init__(self, grid, car_list):
        self.grid = grid
        self.car_list = car_list
    
    def retrieve_value(self, x, y):
        """
        Retrieve value from specified position in the grid.
        """
        return self.grid[y][x]

    def update_value(self, x, y, value):
        """
        Update value at specified position.
        """
        self.grid[y][x] = value
        
    def add_car(self, car):
        """
        Add a car to the board
        """
        index = len(self.car_list)
        self.car_list.append(car)
        
        for i in range(car[1]):
            if car[0] == 'vert':
                self.update_value(car[2], car[3]+i, index)
            elif car[0] == 'hor':
                self.update_value(car[2]+i, car[3], index)

    def move_car(self, car_n, move):
        """
        Move a car through the grid.
        """
	    
	    # Check if move is possible
        if self.check_move_car(car_n, move):
            car = self.car_list[car_n]

            if car[0] == 'hor':
    
                if move == -1:
                    self.update_value(car[2]+car[1]-1, car[3], 0)
                    self.update_value(car[2]-1, car[3], car_n)
                    
                elif move == 1:
                    self.update_value(car[2]+car[1], car[3], car_n)
                    self.update_value(car[2], car[3], 0)
    
                self.car_list[car_n] = self.car_list[car_n][:2] + (self.car_list[car_n][2]+move,) + (self.car_list[car_n][3],)
    
            elif car[0] == 'vert':
                
                if move == -1:
                    self.update_value(car[2], car[3]+car[1]-1, 0)
                    self.update_value(car[2], car[3]-1, car_n)
            
                elif move == 1:
                    self.update_value(car[2], car[3]+car[1], car_n)
                    self.update_value(car[2], car[3], 0)

                self.car_list[car_n] = self.car_list[car_n][:3] + (self.car_list[car_n][3]+move,)

            return True

        else:
            return False

    def check_move_car(self, car_n, move):
        """
        Check if move is possible.
        """
        car = self.car_list[car_n]

        if car[0] == 'hor':
            if move == -1:
                if car[2] > 0:
                    if self.retrieve_value(car[2]-1, car[3]) == 0:
                        return True
            elif move == 1:
                if car[2] + car[1] < len(grid.grid[0]):
                    if self.retrieve_value(car[2]+car[1], car[3]) == 0:
                        return True

        elif car[0] == 'vert':
            if move == -1:
                if car[3] > 0:
                    if self.retrieve_value(car[2], car[3]-1) == 0:
                        return True

            elif move == 1:
                if car[3] + car[1] < len(grid.grid):
                    if self.retrieve_value(car[2], car[3]+car[1]) == 0:
                        return True

        return False

    def check_solution(self):
        """
        Check if the current grid is a valid solution.
        """
        red_car = self.car_list[1]
        if red_car[2]+red_car[1] == len(self.grid):
            return True
        no_path = False
        for i in range(red_car[2]+red_car[1], len(self.grid)):
            if self.grid[red_car[3]][i] != 0:
                no_path = True
                return False
        if no_path == False:
            return True
    

def Car(orientation, length, start_x, start_y):
    """
    Represents a car on the playing board.
    """
    return (orientation, length, start_x, start_y)

