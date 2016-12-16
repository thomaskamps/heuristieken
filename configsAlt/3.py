grid_grid = [[0 for i in range(6)] for j  in range(6)]
grid_car_list = ['placeholder']
grid = Grid(grid_grid, grid_car_list)
grid.add_car(Car('hor', 2, 0, 2)) # red car
grid.add_car(Car('vert', 2, 0, 4))
grid.add_car(Car('vert', 2, 2, 2))
grid.add_car(Car('vert', 2, 2, 4))
grid.add_car(Car('vert', 2, 3, 1))
grid.add_car(Car('vert', 2, 5, 2))
grid.add_car(Car('hor', 2, 1, 0))
grid.add_car(Car('hor', 3, 3, 0))
grid.add_car(Car('hor', 2, 1, 1))
grid.add_car(Car('hor', 2, 4, 1))
grid.add_car(Car('hor', 2, 0, 3))
grid.add_car(Car('hor', 2, 3, 3))
grid.add_car(Car('hor', 2, 4, 4))