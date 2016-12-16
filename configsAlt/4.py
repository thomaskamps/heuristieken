grid_grid = [[0 for i in range(9)] for j  in range(9)]
grid_car_list = ['placeholder']
grid = Grid(grid_grid, grid_car_list)
grid.add_car(Car('hor', 2, 1, 4)) # red car
grid.add_car(Car('vert', 2, 0, 0))
grid.add_car(Car('vert', 2, 0, 4))
grid.add_car(Car('vert', 2, 0, 7))
grid.add_car(Car('vert', 3, 2, 5))
grid.add_car(Car('vert', 3, 3, 1))
grid.add_car(Car('vert', 2, 3, 4))
grid.add_car(Car('vert', 2, 3, 6))
grid.add_car(Car('vert', 2, 4, 7))
grid.add_car(Car('vert', 3, 5, 0))
grid.add_car(Car('vert', 3, 8, 2))
grid.add_car(Car('vert', 3, 8, 5))
grid.add_car(Car('hor', 2, 0, 3))
grid.add_car(Car('hor', 2, 0, 6))
grid.add_car(Car('hor', 3, 1, 8))
grid.add_car(Car('hor', 3, 1, 0))
grid.add_car(Car('hor', 2, 4, 6))
grid.add_car(Car('hor', 3, 5, 3))
grid.add_car(Car('hor', 3, 5, 5))
grid.add_car(Car('hor', 2, 5, 8))
grid.add_car(Car('hor', 3, 6, 1))
grid.add_car(Car('hor', 2, 7, 8))


