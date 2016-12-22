import os
import sys
import pygame
pygame.init()
# Import classes
execfile(os.getcwd() + '/assets/newClasses.py')
execfile(os.getcwd() + '/assets/solver.py')

# Standard variables
screen_width, screen_height = 600, 600
margin = 5
window = pygame.display.set_mode((screen_width + 400, screen_height + margin))

textfont = pygame.font.SysFont("arial", 40)
textfont2 = pygame.font.SysFont("arial", 30)


def update_screen(grids, i, cars, allObjects):
	window.fill(pygame.Color("black"))
	set_controlpanel(log.algo, log.grid, grids, i, cars)				
	allObjects.update()
	draw_grid(grids[i], cars)
	pygame.display.update()
    	
    
# Funciton: Calls the algorithm and laods the configuration for a live calculation
def live_solver(algorithm, configuration):
	# Load selected config and construct grid
    execfile(os.getcwd() + '/configsAlt/' + str(configuration) + '.py', globals())
    solver = Solver(grid.grid, grid.car_list)
    
    # Run algorithm and store return values
    if algorithm == "bfs":
        temp = solver.bfs(grid.grid, grid.car_list)
    elif algorithm == "bestfirst":
        temp = solver.best_first(grid.grid, grid.car_list)
    elif algorithm == "astar":
        temp = solver.a_star(grid.grid, grid.car_list)

	# Construct statelist (shortest path)
    state_list = []
    state_list.append(temp[0].grid)
    current_grid = temp[0].grid
    print len(temp[1])

    while current_grid != grid.grid:
    	temper = temp[1][str(current_grid)]
    	state_list.append(temper)
    	current_grid = temper
    
    return [state_list[::-1], len(temp[1])]


# Function: Create a dictionary that contains for everey car a color code.
def car_color(currentGrid):
    	cars = {}
    	cars[0], cars[1] = (255, 255, 255), (255, 0, 0)
    	for x in currentGrid[0]:
    		for y in x:
    			if y not in cars and y != 0 and y != 1:
    				cars[y] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    	return cars


# Function: Draws a given grid
def draw_grid(grid, cars):
    	grid_width, grid_height = len(grid[0]), len(grid[0])
    	block_size = (screen_width / (grid_width)) - margin
    	border = {6:1, 9:1.75}
        for y in range(grid_height):
            for x in range(grid_width):
                rect = pygame.Rect(border[len(grid)] * margin + x*(block_size + margin), border[len(grid)] * margin + y*(block_size + margin), block_size, block_size)
                pygame.draw.rect(window, cars[grid[y][x]], rect)
        return True

def check_size(length, grids, cars):
	vehicleSize = {}
	for key in cars:
		vehicleSize[key] = 0
		for row in grids[0]:
			for item in row:
				if item == key:
					vehicleSize[key] = vehicleSize[key] + 1
	if length == 0:
		return vehicleSize[0]
	return len([value for key, value in vehicleSize.iteritems() if value == length])


# Function: Draw all the extra elements in the control panel.
def set_controlpanel(alg, config, grids, move, cars):
	pygame.draw.rect(window, (67,190,191), (screen_width + margin, 0, 400, screen_height + margin))
	rect = pygame.draw.rect(window, (37,160,161), (screen_width + 2 * margin, 30 + margin, 160, 60))
	window.blit(textfont.render(str(move) + " / " + str(len(grids)-1), 1, (255,255,255)), (screen_width + 2 * margin + 8, 3 * margin + 40))
	rect = pygame.draw.rect(window, (37,160,161), (screen_width + 2 * margin, 430 + margin, 385, 165))
	window.blit(textfont2.render("Checked States: " + str(data[alg][str(config)]["states"]), 1, (255,255,255)), (screen_width + 3 * margin, 440 + margin))
	window.blit(textfont2.render("Grid Size: " + str(len(grids[0][0])) + " x " + str(len(grids[0])), 1, (255,255,255)), (screen_width + 3 * margin, 470 + margin))
	window.blit(textfont2.render("Cars: " + str(check_size(2, grids, cars)), 1, (255,255,255)), (screen_width + 3 * margin, 500 + margin))
	window.blit(textfont2.render("Trucks: " + str(check_size(3, grids, cars)), 1, (255,255,255)), (screen_width + 3 * margin, 530 + margin))
	window.blit(textfont2.render("White Space : " + str(check_size(0, grids, cars)), 1, (255,255,255)), (screen_width + 3 * margin, 560 + margin))


# Function: Creates all the objects and returns
def create_objects():
    	config1Button = Button()
    	config1Button.index = 1
    	config2Button = Button()
    	config2Button.index = 2
    	config3Button = Button()
    	config3Button.index = 3
    	config4Button = Button()
    	config4Button.index = 4
    	config5Button = Button()
    	config5Button.index = 5
    	config6Button = Button()
    	config6Button.index = 6
    	config7Button = Button()
    	config7Button.index = 7
    	
    	astarButton = Button()
    	astarButton.index = 10
    	astarButton.section = 2
    	astarButton.text = "astar"
    	bestfirstButton = Button()
    	bestfirstButton.index = 20
    	bestfirstButton.section = 2
    	bestfirstButton.text = "bestfirst"
    	bfsButton = Button()
    	bfsButton.index = 30
    	bfsButton.section = 2
    	bfsButton.text = "bfs"
    	
    	playButton = Button()
    	playButton.index = 100
    	playButton.section = 3
    	playButton.text = "P"
    	
    	resetButton = Button()
    	resetButton.index = 200
    	resetButton.section = 3
    	resetButton.text = "R"
    	
    	previousButton = Button()
    	previousButton.index = 300
    	previousButton.section = 3
    	previousButton.text = "<"
    	
    	nextButton = Button()
    	nextButton.index = 400
    	nextButton.section = 3
    	nextButton.text = ">"
    	
    	colorButton = Button()
    	colorButton.index = 500
    	colorButton.section = 3
    	colorButton.text = "C"
    	
    	liveButton = Button()
    	liveButton.index = 1000
    	liveButton.section = 4
    	liveButton.text = "Live"
    	
    	moveLabel = Label()
    	moveLabel.index = 1
    	moveLabel.text = "Move"
    	
    	configLabel = Label()
    	configLabel.index = 2
    	configLabel.text = "Configuration"
    	
    	algoLabel = Label()
    	algoLabel.index = 3
    	algoLabel.text = "Algorithm"
    	
    	controlLabel = Label()
    	controlLabel.index = 4
    	controlLabel.text = "Control"
    	
    	infoLabel = Label()
    	infoLabel.index = 5
    	infoLabel.text = "Info"
    	
    	allObjects = pygame.sprite.Group(config1Button, config2Button, config3Button, config4Button, config5Button, config6Button, config7Button, astarButton, bestfirstButton, bfsButton, playButton, resetButton, previousButton, nextButton, liveButton, moveLabel, configLabel, controlLabel, algoLabel, colorButton, infoLabel)
    	
    	return config1Button, config2Button, config3Button, config4Button, config5Button, config6Button, config7Button, astarButton, bestfirstButton, bfsButton, playButton, resetButton, previousButton, nextButton, liveButton, moveLabel, configLabel, controlLabel, algoLabel, colorButton, infoLabel, allObjects


    	
# Class: Has one instance that keeps track of the current grid en algorithm and livemodus.
class ActiveLog:
		def __init__(self):
			self.grid = 1
			self.algo = ""
			self.live = False
			self.animation = False

log = ActiveLog()


# Class: All the labels in the control panel belongs to this class.
class Label(pygame.sprite.Sprite):
		def __init__(self):
			pygame.sprite.Sprite.__init__(self)
			self.index = 1
			self.text = ""
		
		def update(self):
			window.blit(textfont.render(self.text + ": ", 1, (255,255,255)), (screen_width + 2 * margin, (self.index - 1) * 100 + margin))

# Class: Every button in the control panel belongs to this class.
class Button(pygame.sprite.Sprite):
    	def __init__(self):
    		pygame.sprite.Sprite.__init__(self)
    		self.index = 1
    		self.section = 1
    		self.text = ""
    		
    	def update(self):
    		
    		if self.section == 1:
    			if log.grid == self.index:
    				color = (101,204,156)
    			else:
    				color = (37,160,161)
    			rect = pygame.draw.rect(window, color, (screen_width + (self.index + 1) * margin + (self.index - 1) * 50, 130 + margin, 50, 60))
    			window.blit(textfont.render(str(self.index), 1, (255,255,255)), (screen_width + (self.index + 1) * margin + (self.index-1) * 50 + 18, 130 + margin + 22))
    			
    		if self.section == 2:
    			if log.algo == self.text:
    				color2 = (101,204,156)
    			else:
    				color2 = (37,160,161)
    			rect = pygame.draw.rect(window, (color2), (screen_width + (self.index/10 + 1) * margin + (self.index/10 - 1) * 105, 230 + margin, 105, 60))
    			window.blit(textfont2.render(self.text, 1, (255,255,255)), (screen_width + (self.index/10 + 1) * margin + (self.index/10-1) * 105 + 10, 230 + margin + 22))
    			
    		if self.section == 4:
				if log.live == False:
					color3 = (230,115,87)
				else:
					color3 = (101,204,156)
				rect = pygame.draw.rect(window, (color3), (screen_width + 400 - 100 - 2 * margin, 30 + margin, 100, 60))
				window.blit(textfont.render(self.text, 1, (255,255,255)), (screen_width + self.section*100 - 90, 3 * margin + 40))
    			
    		if self.section == 3:
    			rect = pygame.draw.rect(window, (37,160,161), (screen_width + (self.index/100 + 1) * margin + (self.index/100 - 1) * 50, 330 + margin, 50, 60))
    			window.blit(textfont.render(self.text, 1, (255,255,255)), (screen_width + (self.index/100 + 1) * margin + (self.index/100-1) * 50 + 16, 330 + margin + 22))
    	
    	def pressed(self):
    		pos = pygame.mouse.get_pos()
    		if pygame.draw.rect(window, (255,255,255), (screen_width + (self.index + 1) * margin + (self.index - 1) * 50, 130 + margin, 50, 60)).collidepoint(pos):
    			return True
    		elif pygame.draw.rect(window, (255,255,255), (screen_width + (self.index/10 + 1) * margin + (self.index/10 - 1) * 105, 230 + margin, 105, 60)).collidepoint(pos):
    			return True
    		elif pygame.draw.rect(window, (255,255,255), (screen_width + (self.index/100 + 1) * margin + (self.index/100 - 1) * 50, 330 + margin, 50, 60)).collidepoint(pos):
    			return True
    		elif pygame.draw.rect(window, (255,255,255), (screen_width + self.section*100 - 100 - 2 * margin, 30 + margin, 100, 60)).collidepoint(pos):
    			return True
    		else:
    			return False
        
      