import pygame
import os

os.system('cls')
pygame.init()
pygame.font.init()

# Setup game display
width, height = 400, 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('7 Segment Display')

# Constants
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (63, 0, 0)
FPS = 60
NUMBERS = {
	0: [1, 1, 1, 1, 1, 1, 0],
	1: [0, 1, 1, 0, 0, 0, 0],
	2: [1, 1, 0, 1, 1, 0, 1],
	3: [1, 1, 1, 1, 0, 0, 1],
	4: [0, 1, 1, 0, 0, 1, 1],
	5: [1, 0, 1, 1, 0, 1, 1],
	6: [1, 0, 1, 1, 1, 1, 1],
	7: [1, 1, 1, 0, 0, 0, 0],
	8: [1, 1, 1, 1, 1, 1, 1],
	9: [1, 1, 1, 0, 0, 1, 1]
}

# Variables
number = 0
segments = []
frameCount = 0


class Segment:
	def __init__(self, x, y, w, h):
		"""
		Constructor for Segment object

		Args:
			x (int): x coordinate of Segment
			y (int): y coordinate of Segment
			w (int): width of Segment
			h (int): height of Segment
		"""
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.on = False

	def draw(self, win):
		"""
		Draw Segment on screen

		Args:
			win (Surface): Main display surface
		"""
		color = RED if self.on else DARK_RED
		pygame.draw.rect(win, color, (self.x, self.y, self.w, self.h))


def draw(win):
	"""
	Draw everything to the display

	Args:
		win (Surface): Main display surface
	"""
	win.fill(BLACK)

	for segment in segments:
		segment.draw(win)

	pygame.display.update()


def turnOn(num):
	"""
	'Turn on' specific Segments

	Args:
		num (int): Number to display using 7 Segment Display
	"""
	lst = NUMBERS[num]
	for i, segment in enumerate(segments):
		if lst[i] == 1:
			segment.on = True
		elif lst[i] == 0:
			segment.on = False


# Initialize segments
segments.append(Segment(60, 20, 80, 20))  # A
segments.append(Segment(140, 40, 20, 100))  # B
segments.append(Segment(140, 160, 20, 100))  # C
segments.append(Segment(60, 260, 80, 20))  # D
segments.append(Segment(40, 160, 20, 100))  # E
segments.append(Segment(40, 40, 20, 100))  # F
segments.append(Segment(60, 140, 80, 20))  # G


def main():
	"""
	Main function
	"""
	global number
	global frameCount
	run = True
	clock = pygame.time.Clock()

	while run:
		clock.tick(FPS)
		frameCount += 1

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

			# For changing the displayed number using mouse clicking

			# if event.type == pygame.MOUSEBUTTONDOWN:
			# 	number += 1
			# 	if number == 10:
			# 		number = 0
			# 	turnOn(number)

		# For changing the displayed number automatically
		if frameCount % 1440 == 0:
			number += 1
			if number == 10:
				number = 0
			turnOn(number)

		draw(win)


main()
