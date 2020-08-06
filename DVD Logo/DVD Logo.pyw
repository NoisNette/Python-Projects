import pygame, os, random

os.system('cls')
pygame.init()
pygame.font.init()

width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('DVD Logo')

# Load image and sound
dvd = pygame.image.load('assets/dvd_logo.png')
clack = pygame.mixer.Sound('assets/clack.wav')

# Constants
BLACK = (0, 0, 0)
FPS = 60
clock = pygame.time.Clock()

# Variables
xs, ys = 3, 3
x, y = width // 2 - dvd.get_width() // 2, height // 2 - dvd.get_height() // 2
r, g, b = 255, 255, 255


def move():
	"""
	Function for moving the DVD Logo on the screen, restricting movement and calling to change color
	"""
	global xs, ys, x, y

	x += xs
	y += ys

	if x <= 0 or x + dvd.get_width() >= width:
		xs *= -1
		clack.play()
		changeColor()
	if y <= 0 or y + dvd.get_height() >= height:
		ys *= -1
		clack.play()
		changeColor()

def changeColor():
	"""
	Pick random color and tint the image with it
	"""
	global r, g, b
	r = random.randint(100, 255)
	g = random.randint(100, 255)
	b = random.randint(100, 255)
	
	# Remove all color from image (set image color to BLACK)
	dvd.fill((0, 0, 0), special_flags=pygame.BLEND_MULT)

	# Add color to image
	dvd.fill((r, g, b, 25), special_flags=pygame.BLEND_ADD)
	

def draw(win):
	"""
	Draws everything to the screen

	Args:
		win (pygame.Surface): Main display surface
	"""
	win.fill((0, 0, 0))

	win.blit(dvd, (x, y))

	pygame.display.update()


def main():
	"""
	Main game function
	"""
	run = True

	changeColor()

	while run:
		clock.tick(FPS)

		draw(win)

		#changeColor()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		move()


main()