import pygame
import os

os.system('cls')
pygame.init()
pygame.font.init()

width, height = 800, 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Paint')

# Load image
palette = pygame.transform.scale(pygame.image.load('palette1.jpg'), (300, 300))
palette_rect = palette.get_rect()
palette_rect.x = width - palette.get_width()
palette_rect.y = 500

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 120

w = 10
h = 10
ROWS = (height - palette.get_height()) // h
COLS = width // w

# Variables
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
dragged = False
draw_color = BLACK

class Spot:
	def __init__(self, row, col):
		self.row = row
		self.col = col

		self.w = w
		self.h = h
		self.x = col * w
		self.y = row * h
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

		self.color = WHITE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.w))

	def fill(self):

		
def setColor():
	screen = pygame.display.get_surface()
	mouse = pygame.mouse.get_pos()
	pxarray = pygame.PixelArray(screen)
	pixel = pygame.Color(pxarray[mouse[0], mouse[1]])

	return pixel[1:]

def draw(win):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	# Draw bounds
	pygame.draw.line(win, BLACK, (0, 0), (width, 0), 2)
	pygame.draw.line(win, BLACK, (0, (height - palette.get_height())), (width, (height - palette.get_height())), 2)

	win.blit(palette, palette_rect)

	pygame.display.update()


# Initialize spots
for i in range(ROWS):
	for j in range(COLS):
		grid[i][j] = Spot(i, j)


def main():
	global dragged
	global draw_color

	run = True
	clock = pygame.time.Clock()

	while run:
		clock.tick(FPS)

		draw(win)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				if palette_rect.collidepoint(pygame.mouse.get_pos()):
					draw_color = setColor()

				else:
					dragged = True

			elif event.type == pygame.MOUSEBUTTONUP:
				dragged = False
			
			if event.type == pygame.MOUSEMOTION and dragged:
				for row in grid:
					for spot in row:
						if spot.rect.collidepoint(pygame.mouse.get_pos()):
							spot.color = draw_color
		
main()