import pygame
import os
import random

os.system('cls')
pygame.init()
pygame.font.init()

# Setup game display
width, height = 400, 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Minesweeper')

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIGHT_GREY = (200, 200, 200)
DARK_GREY = (127, 127, 127)
FPS = 60

w = 40  # Width of single spot
rows = height // w
cols = width // w

# Load images and sounds
mine = pygame.transform.scale(pygame.image.load('mine.png'), (w - 5, w - 5))
boom = pygame.mixer.Sound('boom.wav')

# Variables
gameOver = 0


class Spot:
	def __init__(self, i, j, w):
		"""
		Constructor for Spot object

		Args:
			i (int): Spot's row index
			j (int): Spot's column index
			w (int): Width of Spot
		"""
		self.i = i
		self.j = j
		self.x = i * w
		self.y = j * w
		self.w = w
		self.rect = pygame.Rect(self.x, self.y, self.w, self.w)
		self.mine = random.random() < 0.2  # 20% Chance of a spot having a mine
		self.revealed = False
		self.flagged = False
		self.neighbors = 0

	def draw(self, win):
		"""
		Draw Spot on display

		Args:
			win (Surface): Main display surface
		"""
		if self.flagged:  # Draw flag if Spot is flagged
			font = pygame.font.Font(None, w)
			label = font.render('X', 1, RED)
			win.blit(label, (self.x + self.w // 4 + 1, self.y + self.w // 4))

		if self.revealed:  # Overwrite over flag if there is one
			self.flagged = False
			if self.mine:  # Draw mine if present
				win.blit(mine, (self.x + 1, self.y + 1))
			else:  # Draw a blank square and number of neighbors if any
				pygame.draw.rect(win, LIGHT_GREY, (self.x + 1,
                                       self.y + 1, self.w - 1, self.w - 1))

				if self.neighbors > 0:
					font = pygame.font.Font(None, w)
					label = font.render(str(self.neighbors), 1, BLACK)
					win.blit(label, (self.x + self.w // 4 + 2, self.y + self.w // 4 - 2))

		pygame.draw.rect(win, BLACK, self.rect, 1)  # Draw outline of square

	def countNeighbors(self):
		"""
		Count number of Spots around this Spot that have a mine, return if this spot has a mine
		"""
		if self.mine:
			self.neighbors = -1
			return

		total = 0

		for xoff in range(-1, 2):
			for yoff in range(-1, 2):
				i = self.i + xoff
				j = self.j + yoff
				if (i > -1 and i < cols) and (j > -1 and j < rows):
					total += grid[i][j].mine

		self.neighbors = total

	def reveal(self):
		"""
		Reveal self if clicked
		"""
		self.revealed = True

		if self.mine:  # If mine is clicked, game over
			global gameOver
			gameOver = -1

		if self.neighbors == 0:
			self.floodFill()

	def floodFill(self):
		"""
		Reveal all neighbors which don't have mines
		"""
		for xoff in range(-1, 2):
			for yoff in range(-1, 2):
				i = self.i + xoff
				j = self.j + yoff
				if (i > -1 and i < cols) and (j > -1 and j < rows):
					neighbor = grid[i][j]
					if not neighbor.mine and not neighbor.revealed:
						neighbor.reveal()


# Initialize grid
grid = [[Spot(i, j, w) for j in range(cols)] for i in range(rows)]
for row in grid:
	for spot in row:
		spot.countNeighbors()


def draw(win):
	"""
	Draw everything to the screen

	Args:
		win (Surface): Main display surface
	"""
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	pygame.display.update()


def main():
	"""
	Main game function with loop
	"""
	global gameOver
	run = True
	clock = pygame.time.Clock()

	while run:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:  # Left click
					for row in grid:
						for spot in row:
							if spot.rect.collidepoint(pygame.mouse.get_pos()):
								spot.reveal()

				if event.button == 3:  # Right click
					for row in grid:
						for spot in row:
							if spot.rect.collidepoint(pygame.mouse.get_pos()):
								spot.flagged = not spot.flagged

		draw(win)

		# Check if every mine-free spot has been revealed
		gotAll = True
		for row in grid:
			for spot in row:
				if not spot.mine:
					if not spot.revealed:
						gotAll = False
		if gotAll:
			gameOver = 1

		if gameOver:
			run = False


main()

# Reveal all spots
for row in grid:
	for spot in row:
		spot.revealed = True
draw(win)

# Victory
if gameOver == 1:
	font = pygame.font.Font(None, 100)
	label = font.render('YOU WIN!', 1, BLACK)
	win.blit(label, (width // 2 - label.get_width() //
                  2, height // 2 - label.get_height() // 2))

# Loss
if gameOver == -1:
	boom.play()
	font = pygame.font.Font(None, 100)
	label = font.render('YOU LOSE!', 1, BLACK)
	win.blit(label, (width // 2 - label.get_width() //
                  2, height // 2 - label.get_height() // 2))

pygame.display.update()
pygame.time.delay(3000)  # Delay for player to see message and grid
pygame.quit()
quit()
