import pygame
import os
import random

os.system('cls')
pygame.init()
pygame.font.init()

# Setup game display
width, height = 400, 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('2048')

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
w = width // 4


# Grid handling
def blankGrid():
	"""
	Create blank 4x4 grid

	Returns:
		list: 2d list filled with zeroes
	"""
	return [[0 for _ in range(4)] for _ in range(4)]


def flipGrid(grid):
	"""
	Returns the grid passed, flipped on the y axis (|)

	Args:
		grid (list): 2d list

	Returns:
		list: 2d list
	"""
	return [row[::-1] for row in grid]


def rotateGrid(grid):
	"""
	Returns a list with the rows and columns of the passed list swapped

	Args:
		grid (list): 2d list

	Returns:
		list: 2d list
	"""
	newGrid = blankGrid()
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			newGrid[i][j] = grid[j][i]
	return newGrid


def drawGrid(win):
	"""
	Draws the grid lines and numbers to the screen

	Args:
		win (Surface): Main display surface
	"""
	global grid
	for i in range(4):
		for j in range(4):
			# Draw grid squares
			pygame.draw.rect(win, BLACK, (i * w, j * w, w, w), 2)

			# Draw numbers in squares
			val = grid[i][j]
			if val != 0:
				s = str(val)
				length = len(s) - 1
				sizes = [64, 64, 48, 32]

				font = pygame.font.Font(None, sizes[length])
				label = font.render(s, 1, BLACK)
				label_rect = label.get_rect(center=(i * w + w // 2, j * w + w // 2))
				win.blit(label, label_rect)


# Game logic handling
def isGameLost():
	"""
	Checks if the game is lost

	Returns:
		bool: Whether the game is lost
	"""
	global grid
	for i in range(4):
		for j in range(4):
			if grid[i][j] == 0:  # Spot still available
				return False
			# Two identical numbers are adjacent vertically
			if i != 3 and grid[i][j] == grid[i + 1][j]:
				return False
			# Two identical numbers are adjacent horizontally
			if j != 3 and grid[i][j] == grid[i][j + 1]:
				return False
	return True


def isGameWon():
	"""
	Checks if the game is won

	Returns:
		bool: Whether the game is won
	"""
	global grid
	for row in grid:
		if 2048 in grid:  # Win only if a square that has 2048 exists
			return True
	return False


def addNumber():
	"""
	Add a random number to the grid
	"""
	global grid
	options = []
	for i in range(4):
		for j in range(4):
			if grid[i][j] == 0:
				options.append([i, j])  # Get list of empty spots

	if len(options) > 0:
		spot = random.choice(options)
		r = random.random()
		i, j = spot
		grid[i][j] = 2 if r > 0.1 else 4  # 10% chance of 4 else 2


def compare(a, b):
	"""
	Checks if two 2d lists are different

	Args:
		a (list): 2d list
		b (list): 2d list

	Returns:
		bool: Whether the passed in lists are different
	"""
	for i in range(4):
		for j in range(4):
			if a[i][j] != b[i][j]:
				return True
	return False


def slide(row):
	"""
	Slide the elements in the row so there are no 0s in between

	Args:
		row (list): Row of a 2d list

	Returns:
		list: Passed in row with slid elements
	"""
	arr = [el for el in row if el]  # Row with no zeroes
	missing = 4 - len(arr)  # Number of zeroes removed from the original row
	zeroes = [0 for _ in range(missing)]  # List filled with set amount of zeroes
	arr = zeroes + arr
	return arr


def combine(row):
	"""
	Combine identical adjacent numbers into one doubled number and add to score

	Args:
		row (list): Row of a 2d list

	Returns:
		list: Row with identical elements combined
	"""
	global score
	for i in range(3, 0, -1):
		a = row[i]
		b = row[i - 1]
		if a == b:
			row[i] = a + b
			score += row[i]
			row[i - 1] = 0
	return row


def operate(row):
	"""
	Operate on a single row

	Args:
		row (list): Row of a 2d list

	Returns:
		list: Row that has been operated on
	"""
	row = slide(row)
	row = combine(row)
	row = slide(row)
	return row


# Variables
grid = blankGrid()
score = 0
gameOver = False


def keyPressed(key):
	"""
	Function for handling key presses

	Args:
		key (pygame.key): Key that has been pressed
	"""
	global grid
	flipped = False
	rotated = False
	played = True

	if key == pygame.K_DOWN:  # Default case
		# Do nothing
		os.system('cls')

	elif key == pygame.K_UP:
		grid = flipGrid(grid)
		flipped = True

	elif key == pygame.K_RIGHT:
		grid = rotateGrid(grid)
		rotated = True

	elif key == pygame.K_LEFT:
		grid = rotateGrid(grid)
		grid = flipGrid(grid)
		rotated = True
		flipped = True

	else:
		played = False

	if played:
		past = grid[:]
		for i in range(4):
			grid[i] = operate(grid[i])
		changed = compare(past, grid)

		if flipped:
			grid = flipGrid(grid)
		if rotated:
			grid = rotateGrid(grid)
			grid = rotateGrid(grid)
			grid = rotateGrid(grid)
		if changed:
			addNumber()


def draw(win):
	"""
	Draws everything to the screen

	Args:
		win (Surface): Main display surface
	"""
	global gameOver
	win.fill(WHITE)  # Background

	drawGrid(win)

	# Draw score
	font = pygame.font.SysFont('calibri', 48, bold=True)
	label = font.render(str(score), 1, BLACK)
	win.blit(label, (width // 2 - label.get_width() // 2, 5))

	if isGameLost():
		msg = 'YOU LOST!'
		gameOver = True
	elif isGameWon():
		msg = 'YOU WON!'
		gameOver = True

	if gameOver:  # Draw message in the middle of the screen
		font = pygame.font.Font(None, 100)
		label = font.render(msg, 1, BLACK)
		x = width // 2 - label.get_width() // 2
		y = height // 2 - label.get_height() // 2
		win.blit(label, (x, y))

	pygame.display.update()


def main():
	"""
	Main function
	"""
	run = True
	clock = pygame.time.Clock()

	# Add 2 numbers at the beginning
	addNumber()
	addNumber()

	while run:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.KEYDOWN:
				keyPressed(event.key)

		draw(win)

		if gameOver:
			run = False


main()
pygame.time.delay(1500) # Delay to see end-game message
pygame.quit()
quit()
