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

# Load images
dino_idle = pygame.image.load(os.path.join('assets', 'jump.png'))

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
runY = 350
FPS = 60


class Dino:
	def __init__(self):
		self.img = dino_idle
		self.mask = pygame.mask.from_surface(self.img)

		self.x = 150
		self.y = runY - self.img.get_height()
		self.w = self.img.get_width()
		self.h = self.img.get_height()
		self.vel = 0
		self.grav = 1
		self.lift = -15
		self.midair = False

	def draw(self, win):
		self.vel += self.grav
		self.y += self.vel

		if self.y + self.h > runY:
			self.y = runY - self.h
			self.vel = 0

		self.midair = self.y + self.h < runY

		win.blit(self.img, (self.x, self.y))

	def jump(self):
		if not self.midair:
			self.vel += self.lift


class Obstacle:
	def __init__(self):
		self.w = 35
		self.h = random.randint(27, 75)
		self.x = width
		self.y = runY - self.h
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
		self.mask = pygame.mask.from_surface(pygame.Surface((self.w, self.h)))
		self.vel = 7
		self.color = BLACK
		self.hit = False
		self.passed = False

	def draw(self, win):
		self.x -= self.vel
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

		pygame.draw.rect(win, self.color, self.rect)

	def offscreen(self):
		if self.x + self.w < 0:
			obstacles.remove(self)

	def collide(self, dino):
		# TODO Fix collision
		xoff = dino.x - self.x
		yoff = dino.y - self.y
		if self.mask.overlap(dino.mask, (xoff, yoff)) != None:
			self.color = RED
			self.hit = True
		else:
			self.color = BLACK


def draw(win):
	global score
	win.fill(WHITE)

	# Draw ground
	pygame.draw.line(win, BLACK, (0, runY), (width, runY), 4)

	# Draw obstacles
	for obstacle in obstacles:
		obstacle.draw(win)
		obstacle.offscreen()
		obstacle.collide(dino)
	

		# Increment score if obstacle passed and not hit
		if not obstacle.hit and not obstacle.passed:
			if dino.x >= obstacle.x + obstacle.w:
				score += 1
				obstacle.passed = True
		
	# Draw dino
	dino.draw(win)

	# Draw score
	font = pygame.font.Font(None, 64)
	label = font.render('SCORE: {}'.format(score), 1, BLACK)
	win.blit(label, (5, 5))

	pygame.display.update()


# Variables
score = 0
obstacles = []
frameCount = 0

# Objects
dino = Dino()


def main():
	global frameCount
	run = True
	clock = pygame.time.Clock()

	while run:
		clock.tick(FPS)

		draw(win)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					dino.jump()

		if frameCount % 90 == 0:
			obstacles.append(Obstacle())

		frameCount += 1


main()
