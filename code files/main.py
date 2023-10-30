import pygame, sys
from settings import * 
from level import Level
import os


os.chdir("C:/Users/andre/Documents/GitHub/Programmering-projekter/Pygame things/Platformer")

#Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Platformer')
clock = pygame.time.Clock()
pygame.display.list_modes()

#Removing the visibility of the cursor so that a custom one can be used.
pygame.mouse.set_visible(False)

level = Level()

while True:
	#Event loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.fill(BG_COLOR)
	level.run()

	#Drawing logic
	pygame.display.update()
	clock.tick(75)