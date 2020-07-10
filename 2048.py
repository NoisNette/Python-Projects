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
	return [[0 for _ in range(4)] for _ in range(4)]


def copyGrid(grid):
	return grid[:]


def flipGrid(grid):
	return [row[::-1] for row in grid]


def rotateGrid(grid):
	newGrid = blankGrid()
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			newGrid[i][j] = grid[j][i]
	return newGrid


def drawGrid(win):
	global grid
	for i in range(4):
		for j in range(4):
			pygame.draw.rect(win, BLACK, (i * w, j * w, w, w), 2)
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
	global grid
	for i in range(4):
		for j in range(4):
			if grid[i][j] == 0:
				return False
			if i != 3 and grid[i][j] == grid[i + 1][j]:
				return False
			if j != 3 and grid[i][j] == grid[i][j + 1]:
				return False
	return True


def isGameWon():
	global grid
	for row in grid:
		if 2048 in grid:
			return True
	return False


def addNumber():
	global grid
	options = []
	for i in range(4):
		for j in range(4):
			if grid[i][j] == 0:
				options.append([i, j])

	if len(options) > 0:
		spot = random.choice(options)
		r = random.random()
		i, j = spot
		grid[i][j] = 2 if r > 0.1 else 4


def compare(a, b):
	for i in range(4):
		for j in range(4):
			if a[i][j] != b[i][j]:
				return True
	return False


def slide(row):
	arr = [el for el in row if el]
	missing = 4 - len(arr)
	zeroes = [0 for _ in range(missing)]
	arr = zeroes + arr
	return arr


def combine(row):
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
	row = slide(row)
	row = combine(row)
	row = slide(row)
	return row


# Variables
grid = blankGrid()
score = 0
gameOver = False


def keyPressed(key):
	global grid
	flipped = False
	rotated = False
	played = True

	if key == pygame.K_DOWN:
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
		past = copyGrid(grid)
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
	global gameOver
	win.fill(WHITE)

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

	if gameOver:
		font = pygame.font.Font(None, 100)
		label = font.render(msg, 1, BLACK)
		x = width // 2 - label.get_width() // 2
		y = height // 2 - label.get_height() // 2
		win.blit(label, (x, y))

	pygame.display.update()


def main():
	run = True
	clock = pygame.time.Clock()
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
pygame.time.delay(1500)
pygame.quit()
quit()
