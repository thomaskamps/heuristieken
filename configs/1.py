grid_grid = [[0 for i in range(6)] for j  in range(6)]
grid_car_list = ['placeholder']
grid = Grid(grid_grid, grid_car_list)
grid.add_car(Car('hor', 2, 3, 2)) # red car
grid.add_car(Car('vert', 3, 2, 0))
grid.add_car(Car('vert', 3, 5, 0))
grid.add_car(Car('vert', 3, 3, 3))
grid.add_car(Car('vert', 2, 0, 4))
grid.add_car(Car('hor', 2, 1, 4))
grid.add_car(Car('hor', 2, 3, 0))
grid.add_car(Car('hor', 2, 4, 3))
grid.add_car(Car('hor', 2, 4, 5))
