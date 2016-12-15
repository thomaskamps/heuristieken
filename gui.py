import pygame
import sys
import random
import os
execfile(os.getcwd() + '/data.py')
execfile(os.getcwd() + '/assets/solver.py')
execfile(os.getcwd() + '/rushHourSolverGui.py')

def draw_solution(grids):    
    pygame.init()
    
    #--------------------------------------------
    # Set initial grid.
    if grids == []:
    	grids = data["astar"]["1"]["path"][::-1]
    
    #--------------------------------------------
    # Set standard variables.
    grid_width, grid_height = len(grids[0]), len(grids[0])
    margin = 5
    screen_width, screen_height = 600, 600
    block_size = (screen_width / (grid_width)) - margin
    textfont = pygame.font.SysFont("arial", 40)
    textfont2 = pygame.font.SysFont("arial", 30)
    
    global animation
    animation = False
    
    window = pygame.display.set_mode((screen_width + 400, screen_height + margin))
    i = 0
    delay = int(0.5 * 1000)

	#--------------------------------------------
    # Set colors for each car in grid.
    cars = {}
    
    def car_color(currentGrid):
    	cars[0], cars[1] = (255, 255, 255), (255, 0, 0)
    	for x in currentGrid[0]:
    		for y in x:
    			if y not in cars and y != 0 and y != 1:
    				cars[y] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    car_color(grids)
    
    #--------------------------------------------
    # Draw grid function.
    def draw_grid(grid):
    	grid_width, grid_height = len(grids[0]), len(grids[0])
    	block_size = (screen_width / (grid_width)) - margin
        for y in range(grid_height):
            for x in range(grid_width):
                rect = pygame.Rect(margin + x*(block_size + margin), margin + y*(block_size + margin), block_size, block_size)
                pygame.draw.rect(window, cars[grid[y][x]], rect)
        return True
    draw_grid(grids[i])
    
    #--------------------------------------------
    # Button class.
    class Button(pygame.sprite.Sprite):
    	def __init__(self):
    		pygame.sprite.Sprite.__init__(self)
    		self.index = 1
    		self.section = 1
    		self.text = ""
    		
    	def update(self):
    		
    		if self.section == 1:
    			if activeGrid == self.index:
    				color = (101,204,156)
    			else:
    				color = (37,160,161)
    			rect = pygame.draw.rect(window, color, (screen_width + (self.index + 1) * margin + (self.index - 1) * 50, 130 + margin, 50, 60))
    			window.blit(textfont.render(str(self.index), 1, (255,255,255)), (screen_width + (self.index + 1) * margin + (self.index-1) * 50 + 18, 130 + margin + 22))
    			
    		if self.section == 2:
    			if activeAlgo == self.text:
    				color2 = (101,204,156)
    			else:
    				color2 = (37,160,161)
    			rect = pygame.draw.rect(window, (color2), (screen_width + (self.index/10 + 1) * margin + (self.index/10 - 1) * 105, 230 + margin, 105, 60))
    			window.blit(textfont2.render(self.text, 1, (255,255,255)), (screen_width + (self.index/10 + 1) * margin + (self.index/10-1) * 105 + 10, 230 + margin + 22))
    			
    		if self.section == 4:
				if liveModus == False:
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
					
	#--------------------------------------------
    # Label class.
    class Label(pygame.sprite.Sprite):
		def __init__(self):
			pygame.sprite.Sprite.__init__(self)
			self.index = 1
			self.text = ""
		
		def update(self):
			window.blit(textfont.render(self.text + ": ", 1, (255,255,255)), (screen_width + 2 * margin, (self.index - 1) * 100 + margin))
    
    #--------------------------------------------
    def set_controlpanel(alg, config):
    	pygame.draw.rect(window, (67,190,191), (screen_width + margin, 0, 400, screen_height + margin))
    	rect = pygame.draw.rect(window, (37,160,161), (screen_width + 2 * margin, 30 + margin, 100, 60))
    	window.blit(textfont.render(str(i) + " / " + str(len(grids)-1), 1, (255,255,255)), (screen_width + 2 * margin + 8, 3 * margin + 40))
    	rect = pygame.draw.rect(window, (37,160,161), (screen_width + 2 * margin, 430 + margin, 385, 165))
    	window.blit(textfont2.render("Checked States: " + str(data[alg][str(config)]["states"]), 1, (255,255,255)), (screen_width + 3 * margin, 440 + margin))
    	window.blit(textfont2.render("Grid Size: " + str(len(grids[0][0])) + " x " + str(len(grids[0])), 1, (255,255,255)), (screen_width + 3 * margin, 470 + margin))
    	window.blit(textfont2.render("Cars: " + str(check_size(2)), 1, (255,255,255)), (screen_width + 3 * margin, 500 + margin))
    	window.blit(textfont2.render("Trucks: " + str(check_size(3)), 1, (255,255,255)), (screen_width + 3 * margin, 530 + margin))
    	window.blit(textfont2.render("White Space : " + str(check_size(0)), 1, (255,255,255)), (screen_width + 3 * margin, 560 + margin))
    
    #--------------------------------------------
    def check_size(length):
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
    	
    
    #--------------------------------------------
    # Creating all objects.
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
    
    set_controlpanel("astar", 1)
    
    allObjects = pygame.sprite.Group(config1Button, config2Button, config3Button, config4Button, config5Button, config6Button, config7Button, astarButton, bestfirstButton, bfsButton, playButton, resetButton, previousButton, nextButton, liveButton, moveLabel, configLabel, controlLabel, algoLabel, colorButton, infoLabel)
    
    #--------------------------------------------
    # Main program.
    activeGrid = 1
    activeAlgo = "astar"
    liveModus = False
    allObjects.update()
    while True:
    	pygame.display.set_caption("Multi Turbo Rush Hour Solver")
        for event in pygame.event.get():
        	if event.type == pygame.QUIT:
        		pygame.quit()
        		sys.exit()
        	if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if config1Button.pressed():
					liveModus = False
					grids = data[activeAlgo]["1"]["path"][::-1]
					car_color(grids)
					i = 0
					activeGrid = 1
				if config2Button.pressed():
					liveModus = False
					grids = data[activeAlgo]["2"]["path"][::-1]
					car_color(grids)
					i = 0
					activeGrid = 2
				if config3Button.pressed():
					liveModus = False
					grids = data[activeAlgo]["3"]["path"][::-1]
					car_color(grids)
					i = 0
					activeGrid = 3
				if config4Button.pressed():
					liveModus = False
					grids = data[activeAlgo]["4"]["path"][::-1]
					car_color(grids)
					i = 0
					activeGrid = 4
				if config6Button.pressed():
					liveModus = False
					grids = data[activeAlgo]["6"]["path"][::-1]
					car_color(grids)
					i = 0
					activeGrid = 6
				
				if liveButton.pressed():
					global liveModus
					if liveModus == False:
						global liveModus
						liveModus = True
					else:
						global liveModus
						liveModus = False
					print activeGrid
					grids = live_solver(activeAlgo, activeGrid)[0]
									
				if astarButton.pressed():
					liveModus = False
					activeAlgo = "astar"
					grids = data[activeAlgo][str(activeGrid)]["path"][::-1]
				if bestfirstButton.pressed():
					liveModus = False
					activeAlgo = "bestfirst"
					grids = data[activeAlgo][str(activeGrid)]["path"][::-1]
								
				if playButton.pressed():
					global animation
					if animation == False:
						global animation
						print animation
						animation = True
					else:
						global animation
						print animation
						animation = False
				
				if resetButton.pressed():
					i = 0
					animation = False
					window.fill(pygame.Color("black"))
				
				if previousButton.pressed():
					if animation == False and i > 0:
						i -= 1
						
				if nextButton.pressed():
					if animation == False and i >= 0 and i < len(grids) - 1:
						i += 1
				
				if colorButton.pressed():
					cars = {}
					car_color(grids)
				
				window.fill(pygame.Color("black"))
				set_controlpanel(activeAlgo, activeGrid)				
				allObjects.update()
				draw_grid(grids[i])
				pygame.display.update()
			
		# Animation.
        if i < len(grids) - 1 and animation == True:
            i = i + 1
            set_controlpanel(activeAlgo, activeGrid)
            window.blit(textfont.render(str(i) + " / " + str(len(grids)-1), 1, (255,255,255)), (screen_width + 2 * margin + 8, 3 * margin + 40))
            allObjects.update()
            draw_grid(grids[i])
            pygame.time.delay(delay)
        
        if i == len(grids) - 1:
        	animation = False
        
        pygame.display.update()


draw_solution([])