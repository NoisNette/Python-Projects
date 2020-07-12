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
ground = pygame.image.load(os.path.join('assets', 'floor-1.png'))
ground = pygame.transform.scale(ground, (width, ground.get_height()))

dino_jump = pygame.image.load(os.path.join('assets', 'jump.png'))

dino_run = []
dino_run.append(pygame.image.load(os.path.join('assets', 'run1.png')))
dino_run.append(pygame.image.load(os.path.join('assets', 'run2.png')))

dino_duck = []
dino_duck.append(pygame.image.load(os.path.join('assets', 'low1small.png')))
dino_duck.append(pygame.image.load(os.path.join('assets', 'low2small.png')))

cactus1 = pygame.image.load(os.path.join('assets', 'CACTUS1.png'))


# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
runY = 350
FPS = 60

# Variables
score = 0
obstacles = []
frameCount = 0
animation_count = 0


class Dino:
	def __init__(self):
		self.img = dino_run[animation_count]
		self.mask = pygame.mask.from_surface(self.img)

		self.x = 150
		self.y = runY - self.img.get_height()
		self.w = self.img.get_width()
		self.h = self.img.get_height()
		self.vel = 0
		self.grav = 1
		self.lift = -15
		self.midair = False
		self.ducked = False

	def draw(self, win):
		global animation_count
		self.vel += self.grav
		self.y += self.vel

		if self.y + self.h > runY:
			self.y = runY - self.h
			self.vel = 0

		self.midair = self.y + self.h < runY

		if self.midair:
			self.img = dino_jump
		elif self.ducked:
			self.img = dino_duck[animation_count]
			self.y = runY - self.img.get_height() + 4
		else:
			self.img = dino_run[animation_count]

		win.blit(self.img, (self.x, self.y))

	def jump(self):
		if not self.midair:
			self.vel += self.lift

	def duck(self):
		if not self.midair:
			self.ducked = True
   
	def unduck(self):
		self.ducked = False


class Obstacle:
	def __init__(self):
		self.img = cactus1
		self.mask = pygame.mask.from_surface(self.img)

		self.w = self.img.get_width()
		self.h = self.img.get_height()
		self.x = width
		self.y = runY - self.h

		self.vel = 7
		self.hit = False
		self.passed = False

	def draw(self, win):
		self.x -= self.vel

		win.blit(self.img, (self.x, self.y))

		# Check for offscreen
		if self.x + self.w < 0:
			obstacles.remove(self)

	def collide(self, dino):
		xoff = dino.x - self.x
		yoff = dino.y - self.y
		if self.mask.overlap(dino.mask, (xoff, yoff)) != None:
			self.hit = True


def draw(win):
	global score
	win.fill(WHITE)

	# Draw ground
	win.blit(ground, (0, runY))

	# Draw obstacles
	for obstacle in obstacles:
		obstacle.draw(win)
		obstacle.collide(dino)

		# Increment score if obstacle passed and not hit
		if not obstacle.hit and not obstacle.passed:
			if dino.x >= obstacle.x + obstacle.w:
				score += 1
				obstacle.passed = True  # Make sure every obstacle is only counted once

	# Draw dino
	dino.draw(win)

	# Draw score
	font = pygame.font.Font(None, 64)
	label = font.render('SCORE: {}'.format(score), 1, BLACK)
	win.blit(label, (5, 5))

	pygame.display.update()


# Objects
dino = Dino()


def main():
	global frameCount
	global animation_count
	run = True
	clock = pygame.time.Clock()

	while run:
		clock.tick(FPS)

		draw(win)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
					dino.jump()

				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					dino.duck()

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					dino.unduck()

		if frameCount % 60 == 0:
			obstacles.append(Obstacle())

		if frameCount % 10 == 0:
			animation_count = (animation_count + 1) % 2

		frameCount += 1


main()
