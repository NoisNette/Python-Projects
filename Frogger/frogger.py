import pygame, os, Rectangle, Frog, Car

os.system('cls')
pygame.init()
pygame.font.init()

# Setup game display
width, height = 640, 480
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Frogger')

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
clock = pygame.time.Clock()

# Objects
frog = Frog.Frog(100, 100, 100)


def draw(win):
	win.fill(BLACK)

	frog.draw(win)

	pygame.display.update()


def main():
	run = True

	while run:
		clock.tick(FPS)

		draw(win)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
		

main()