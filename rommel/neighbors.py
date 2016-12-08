def find_neighbors(grid, carnumber):
	carlist = []
	for row in grid:
		for car in row:
			if car not in carlist:
				carlist.append(car)
	carlist.remove(0)
	
	
	neighborsdict = {}
	for car in carlist:
		neighborsdict[car] = []
	
	for car in carlist:
		for row in grid:
			if car in row:
				for i in range(len(row)-1):
					if row[i] == car or row[i+1] == car:
						if row[i] != 0 and row[i+1] != 0:
							if row[i] not in neighborsdict[car] and row[i] != car:
								neighborsdict[car].append(row[i])
							if row[i+1] not in neighborsdict[car] and row[i+1] != car:
								neighborsdict[car].append(row[i+1])
									
	for car in carlist:
		for i in range(len(grid)):
			if car in grid[i]:
				carindexes = [j for j, x in enumerate(grid[i]) if x == car]
				for index in carindexes:
					
					if i != 0:
						if grid[i-1][index] not in neighborsdict[car]:
							if grid[i-1][index] != 0 and grid[i-1][index] != car:
								neighborsdict[car].append(grid[i-1][index])
					
					if i != 5:
						if grid[i+1][index] not in neighborsdict[car]:
							if grid[i-1][index] != 0 and grid[i-1][index] != car:
								neighborsdict[car].append(grid[i+1][index])
						
						
	print "------------------------"
	print neighborsdict
	for row in grid:
		print row
	print "------------------------"			

	return neighborsdict[carnumber]

find_neighbors([[6, 6, 7, 7, 4, 0], [8, 8, 9, 9, 4, 0], [0, 0, 0, 0, 1, 1], [10, 10, 0, 11, 11, 5], [2, 12, 12, 3, 0, 5], [2, 13, 13, 3, 0, 5]], 1)