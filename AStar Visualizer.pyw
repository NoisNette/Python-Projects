import pygame
import os

os.system('cls')
pygame.init()
pygame.font.init()

width, height = 800, 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('A* Pathfinder Visualizer')

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 255, 0)
GREEN = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

FPS = 60
NUM_ROWS = 16
w = width // NUM_ROWS
grid = [[0 for _ in range(NUM_ROWS)] for _ in range(NUM_ROWS)]


class Spot:
	def __init__(self, row, col):
		self.row = row
		self.col = col
		self.w = w
		self.x = w * col
		self.y = w * row
		self.color = WHITE
	
	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.w))
		pygame.draw.rect(win, BLACK, (self.x, self.y, self.w, self.w), 2)


# Initialize all spots
for i in range(NUM_ROWS):
	for j in range(NUM_ROWS):
		grid[i][j] = Spot(i, j)


def draw(win):
	for row in grid:
		for spot in row:
			spot.draw(win)

	pygame.display.update()


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