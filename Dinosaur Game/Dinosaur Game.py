import pygame
import os
import random

os.system('cls')
pygame.init()
pygame.font.init()

# Setup game display
width, height = 900, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Dinosaur Game')


class Dino:
	def __init__(self):
		self.r = 16
		self.x = 150
		self.y = 350 - self.r

	def draw(self, win):
		pygame.draw.circle(win, BLACK, (self.x, self.y), self.r)


class Obstacle:
	def __init__(self):
		pass


def draw(win):
	win.fill(WHITE)

	# Draw ground
	pygame.draw.rect(win, BLACK, (0, 350, width, 10))

	dino.draw(win)

	pygame.display.update()


# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60

# Variables
score = 0
obstacles = []

# Objects
dino = Dino()


def main():
	run = True
	clock = pygame.time.Clock()

	while run:
		clock.tick(FPS)

		draw(win)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()


main()
