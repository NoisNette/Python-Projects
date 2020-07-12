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
ground = pygame.image.load(os.path.join('assets', 'floor-1.png')).convert()
ground_img = pygame.transform.scale(ground, (width, ground.get_height()))

dino_jump = pygame.image.load(os.path.join('assets', 'jump.png'))

dino_run = []
dino_run.append(pygame.image.load(os.path.join('assets', 'run1.png')))
dino_run.append(pygame.image.load(os.path.join('assets', 'run2.png')))

dino_duck = []
dino_duck.append(pygame.image.load(os.path.join('assets', 'low1.png')))
dino_duck.append(pygame.image.load(os.path.join('assets', 'low2.png')))

dino_death = pygame.image.load(os.path.join('assets', 'death.png'))

cactuses = []
for i in range(1, 6):
	cactus = pygame.image.load(os.path.join('assets', 'CACTUS{}.png'.format(i)))
	cactuses.append(cactus)

enemies = []
enemies.append(pygame.image.load(os.path.join('assets', 'enemy1.png')))
enemies.append(pygame.image.load(os.path.join('assets', 'enemy2.png')))

retry_img = pygame.transform.scale(pygame.image.load(os.path.join('assets', '1x-restart.png')), (64, 57))

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
velocity = 7
ground1_x = 0
ground2_x = width
gameOver = False


class Dino:
	def __init__(self):
		self.img = dino_run[animation_count]
		self.mask = pygame.mask.from_surface(self.img)

		self.x = 150
		self.y = runY - self.img.get_height() + 4
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
			self.y = runY - self.img.get_height() + 2
		else:
			self.img = dino_run[animation_count]

		if gameOver:
			self.img = dino_death

		win.blit(self.img, (self.x, self.y))

	def jump(self):
		if not self.midair:
			self.vel += self.lift

	def duck(self):
		if not self.midair:
			self.ducked = True


class Cactus:
	def __init__(self):
		self.img = self.chooseCactusImage()
		self.mask = pygame.mask.from_surface(self.img)

		self.w = self.img.get_width()
		self.h = self.img.get_height()
		self.x = width
		self.y = runY - self.h + 5

		self.hit = False
		self.passed = False

	def draw(self, win):
		self.x -= velocity

		win.blit(self.img, (self.x, self.y))

		# Check for offscreen
		if self.x + self.w < 0:
			obstacles.remove(self)

	def collide(self, dino):
		xoff = dino.x - self.x
		yoff = dino.y - self.y
		if self.mask.overlap(dino.mask, (xoff, yoff)) != None:
			self.hit = True

	def chooseCactusImage(self):
		perc = random.random()
		if perc > 0.9:
			return cactuses[-1]
		else:
			return random.choice(cactuses[:-1])

class Enemy:
	def __init__(self):
		self.img = enemies[animation_count]
		self.mask = pygame.mask.from_surface(self.img)

		self.w = self.img.get_width()
		self.h = self.img.get_height()
		self.x = width
		self.y = self.getHeight()

		self.hit = False
		self.passed = False

	def draw(self, win):
		self.x -= velocity

		self.img = enemies[animation_count]

		win.blit(self.img, (self.x, self.y))

		# Check for offscreen
		if self.x + self.w < 0:
			obstacles.remove(self)

	def collide(self, dino):
		xoff = dino.x - self.x
		yoff = dino.y - self.y
		if self.mask.overlap(dino.mask, (xoff, yoff)) != None:
			self.hit = True

	def getHeight(self):
		y = runY - self.h
		gap = random.choice([0, 45, 65])
		return y - gap


def drawGround(win):
	global ground1_x
	global ground2_x

	ground1_x -= velocity
	ground2_x -= velocity

	if ground1_x < -width:
		ground1_x = width
	
	if ground2_x < -width:
		ground2_x = width

	win.blit(ground_img, (ground1_x, runY))
	win.blit(ground_img, (ground2_x, runY))


def draw(win):
	win.fill(WHITE)

	# Draw ground
	drawGround(win)

	# Draw obstacles
	for obstacle in obstacles:
		obstacle.draw(win)
		obstacle.collide(dino)

		# Increment score if obstacle passed and not hit
		if not obstacle.hit and not obstacle.passed:
			if dino.x >= obstacle.x + obstacle.w:
				obstacle.passed = True  # Make sure every obstacle is only counted once

	# Draw dino
	dino.draw(win)

	# Draw score
	score_display = str(score).rjust(5, '0')
	font = pygame.font.Font('assets/font/pixelmix.ttf', 24)
	label = font.render(score_display, 1, BLACK)
	win.blit(label, (5, 5))

	pygame.display.update()


# Objects
dino = Dino()


def main():
	global frameCount
	global animation_count
	global score
	global velocity
	global gameOver

	run = True
	clock = pygame.time.Clock()

	while run:
		clock.tick(FPS)

		for obstacle in obstacles:
			if obstacle.hit:
				gameOver = True
				velocity = 0
				run = False

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
					dino.ducked = False


		if not gameOver:
			# Add a new obstacle every second
			if frameCount % 60 == 0:
				obstacle_choices = [Cactus(), Cactus(), Cactus()]

				if score > 200: # 25% Possibility of Pterodactyl obstacle after 200 points
					obstacle_choices.append(Enemy())

				obstacles.append(random.choice(obstacle_choices))

			# Animation
			if frameCount % 10 == 0:
				animation_count = (animation_count + 1) % 2

			# Incrementing score
			if frameCount % 5 == 0:
				score += 1

			frameCount += 1



main()
pygame.time.delay(750)