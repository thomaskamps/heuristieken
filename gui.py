import pygame
import sys
import random
import os

execfile(os.getcwd() + '/assets/data.py')
execfile(os.getcwd() + '/assets/solver.py')
execfile(os.getcwd() + '/assets/gui_helper.py')

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
 
    window = pygame.display.set_mode((screen_width + 400, screen_height + margin))
    i = 0
    delay = int(0.5 * 1000)

    cars = car_color(grids)
    draw_grid(grids[i], cars)
    
    config1Button, config2Button, config3Button, config4Button, config5Button, config6Button, config7Button, astarButton, bestfirstButton, playButton, resetButton, previousButton, nextButton, liveButton, moveLabel, configLabel, controlLabel, algoLabel, colorButton, infoLabel, allObjects = create_objects()
    
    set_controlpanel("astar", 1, grids, i, cars)

    log.grid = 1
    log.algo = "astar"
    log.live = False
    log.animation = False
    
    allObjects.update()
    

    
    while True:
    	pygame.display.set_caption("Multi Turbo Rush Hour Solver")
        for event in pygame.event.get():
        	if event.type == pygame.QUIT:
        		pygame.quit()
        		sys.exit()
        	
        	if event.type == pygame.KEYDOWN:
        	 	if event.key == pygame.K_LEFT:
        	 		if log.animation == False and i > 0:
        	 			i -= 1
        	 	if event.key == pygame.K_RIGHT:
        	 		if log.animation == False and i >= 0 and i < len(grids) - 1:
        	 			i += 1
        	 		
        	if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if config1Button.pressed():
					log.live = False
					grids = data[log.algo]["1"]["path"][::-1]
					cars = car_color(grids)
					i = 0
					log.grid = 1
				if config2Button.pressed():
					log.live = False
					grids = data[log.algo]["2"]["path"][::-1]
					cars = car_color(grids)
					i = 0
					log.grid = 2
				if config3Button.pressed():
					log.live = False
					grids = data[log.algo]["3"]["path"][::-1]
					cars = car_color(grids)
					i = 0
					log.grid = 3
				if config4Button.pressed():
					log.live = False
					grids = data[log.algo]["4"]["path"][::-1]
					cars = car_color(grids)
					i = 0
					log.grid = 4
				if config5Button.pressed():
					log.live = False
					grids = data[log.algo]["5"]["path"][::-1]
					cars = car_color(grids)
					i = 0
					log.grid = 5
				if config6Button.pressed():
					log.live = False
					grids = data[log.algo]["6"]["path"][::-1]
					cars = car_color(grids)
					i = 0
					log.grid = 6
				
				if liveButton.pressed():
					if log.live == False:
						log.live = True
					else:
						log.live = False
					grids = live_solver(log.algo, log.grid)[0]
									
				if astarButton.pressed():
					log.live = False
					log.algo = "astar"
					grids = data[log.algo][str(log.grid)]["path"][::-1]
				if bestfirstButton.pressed():
					log.live = False
					log.algo = "bestfirst"
					grids = data[log.algo][str(log.grid)]["path"][::-1]
								
				if playButton.pressed():
					if log.animation == False:
						log.animation = True
					else:
						log.animation = False
				
				if resetButton.pressed():
					i = 0
					log.animation = False
					window.fill(pygame.Color("black"))
				
				if previousButton.pressed():
					if log.animation == False and i > 0:
						i -= 1
						
				if nextButton.pressed():
					if log.animation == False and i >= 0 and i < len(grids) - 1:
						i += 1
				
				if colorButton.pressed():
					cars = {}
					cars = car_color(grids)
				
				update_screen(grids, i, cars, allObjects)
			
        if i < len(grids) - 1 and log.animation == True:
            i = i + 1
            
            window.blit(textfont.render(str(i) + " / " + str(len(grids)-1), 1, (255,255,255)), (screen_width + 2 * margin + 8, 3 * margin + 40))
            update_screen(grids, i, cars, allObjects)
            
            pygame.time.delay(delay)
        
        if i == len(grids) - 1:
        	log.animation = False
        
        pygame.display.update()


draw_solution([])