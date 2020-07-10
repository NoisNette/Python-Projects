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

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
runY = 350
FPS = 60


class Dino:
	def __init__(self):
		self.r = 16
		self.x = 150
		self.y = runY - self.r
		self.vel = 0
		self.grav = 1
		self.lift = -15
		self.midair = False

	def draw(self, win):
		self.vel += self.grav
		self.y += self.vel

		if self.y + self.r > runY:
			self.y = runY - self.r
			self.vel = 0

		self.midair = self.y + self.r < runY

		pygame.draw.circle(win, BLACK, (self.x, self.y), self.r)

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
		self.vel = 3
	
	def draw(self, win):
		self.x -= self.vel
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

		pygame.draw.rect(win, BLACK, self.rect)
	
	def offscreen(self):
		if self.x + self.w < 0:
			obstacles.remove(self)


def draw(win):
	win.fill(WHITE)

	# Draw ground
	pygame.draw.line(win, BLACK, (0, runY), (width, runY), 4)

	# Draw dino
	dino.draw(win)
	
	# Draw obstacles
	for obstacle in obstacles:
		obstacle.draw(win)
		obstacle.offscreen()

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
		
		if frameCount % 120 == 0:
			obstacles.append(Obstacle())

		frameCount += 1

main()
