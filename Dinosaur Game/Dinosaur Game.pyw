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

# Variables
score = 0
obstacles = []
frameCount = 0
animation_count = 0
velocity = 7
ground1_x = 0
ground2_x = width
fps = 60
gameOver = False


class Dino:
	def __init__(self):
		"""
		Constructor for Dino class
		"""
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
		"""
		Draw Dino to screen

		:param win: Main display surface
		:type win: Surface
		"""
		global animation_count

		# Apply gravity
		self.vel += self.grav
		self.y += self.vel

		# Don't let dino fall down
		if self.y + self.h > runY:
			self.y = runY - self.h
			self.vel = 0

		# Check if dino is midair
		self.midair = self.y + self.h < runY

		if self.midair:
			self.img = dino_jump  # Image if dino is midair
		elif self.ducked:
			self.img = dino_duck[animation_count]
			self.y = runY - self.img.get_height() + 2  # Lower y position to account for ducking
		else:
			self.img = dino_run[animation_count]  # Regular running image

		if gameOver:
			self.img = dino_death  # Death image if game is over

		win.blit(self.img, (self.x, self.y))

	def jump(self):
		"""
		Apply jump force to dino
		"""
		if not self.midair:
			self.vel += self.lift

	def duck(self):
		"""
		Duck the dino if not midair
		"""
		if not self.midair:
			self.ducked = True


class Cactus:
	def __init__(self):
		"""
		Constructor for Cactus class
		"""
		self.img = self.chooseCactusImage()
		self.mask = pygame.mask.from_surface(self.img)

		self.w = self.img.get_width()
		self.h = self.img.get_height()
		self.x = width
		self.y = runY - self.h + 5

		self.hit = False
		self.passed = False

	def draw(self, win):
		"""
		Draw Cactus to the screen

		:param win: Main display surface
		:type win: Surface
		"""

		# Move cactus
		self.x -= velocity

		win.blit(self.img, (self.x, self.y))

		# Check for offscreen
		if self.x + self.w < 0:
			obstacles.remove(self)

	def collide(self, dino):
		"""
		Check if cactus collides with dino

		:param dino: Dinosaur object
		:type dino: Dino
		"""

		# Calculate distance between top left points for self and dino, used for mask.overlap
		xoff = dino.x - self.x
		yoff = dino.y - self.y
		if self.mask.overlap(dino.mask, (xoff, yoff)) != None:
			self.hit = True

	def chooseCactusImage(self):
		"""
		Determine what cactus will be spawned

		:return: Image of this cactus
		:rtype: Surface
		"""
		perc = random.random()
		if perc > 0.75:  # 25 % of triple-cactus spawning
			return cactuses[-1]
		else:
			return random.choice(cactuses[:-1])

class Enemy:
	def __init__(self):
		"""
		Constructor for Enemy class (Pterodactyl)
		"""
		self.img = enemies[animation_count]
		self.mask = pygame.mask.from_surface(self.img)

		self.w = self.img.get_width()
		self.h = self.img.get_height()
		self.x = width
		self.y = self.getHeight()

		self.hit = False
		self.passed = False

	def draw(self, win):
		"""
		Draw Enemy to the screen

		:param win: Main display surface
		:type win: Surface
		"""

		# Move pterodactyl
		self.x -= velocity

		# Update image
		self.img = enemies[animation_count]

		win.blit(self.img, (self.x, self.y))

		# Check for offscreen
		if self.x + self.w < 0:
			obstacles.remove(self)

	def collide(self, dino):
		"""
		Check if enemy collides with dino

		:param dino: Dinosaur object
		:type dino: Dino
		"""

		# Calculate distance between top left points for self and dino, used for mask.overlap
		xoff = dino.x - self.x
		yoff = dino.y - self.y
		if self.mask.overlap(dino.mask, (xoff, yoff)) != None:
			self.hit = True

	def getHeight(self):
		"""
		Get height on which the pterodactyl will be

		:return: y coordinate of self
		:rtype: int
		"""
		y = runY - self.h
		gap = 10 if random.random() > 0.75 else random.choice([45, 75])  # 25 % Chance of pterodactyl on ground
		return y - gap


def drawGround(win):
	"""
	Draw and animate ground using 2 consecutive identical images

	:param win: Main display surface
	:type win: Surface
	"""
	global ground1_x
	global ground2_x

	# Move both ground images
	ground1_x -= velocity
	ground2_x -= velocity

	# Reset position of ground images
	if ground1_x < -width:
		ground1_x = width
	if ground2_x < -width:
		ground2_x = width

	# Display both images
	win.blit(ground_img, (ground1_x, runY))
	win.blit(ground_img, (ground2_x, runY))


def draw(win):
	"""
	Draw everything to the screen

	:param win: Main display surface
	:type win: Surface
	"""
	win.fill(WHITE)

	# Draw ground
	drawGround(win)

	# Draw obstacles
	for obstacle in obstacles:
		obstacle.draw(win)
		obstacle.collide(dino)


	# Draw dino
	dino.draw(win)

	# Draw score
	score_display = str(score).rjust(5, '0')  # Pad score to width of 5
	font = pygame.font.Font('assets/font/pixelmix.ttf', 24)
	label = font.render(score_display, 1, BLACK)
	win.blit(label, (5, 5))

	pygame.display.update()


# Objects
dino = Dino()


def main():
	"""
	Main function
	"""
	global frameCount
	global animation_count
	global score
	global velocity
	global fps
	global gameOver

	run = True
	clock = pygame.time.Clock()

	while run:
		clock.tick(fps)

		# Check for game over if any obstacle is hit
		for obstacle in obstacles:
			if obstacle.hit:
				gameOver = True
				velocity = 0
				run = False

		draw(win)

		# Event loop
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.KEYDOWN:
				# Jump if space, 'W' or up_arrow are pressed
				if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
					dino.jump()

				# Duck if 'S' or down_arrow are pressed
				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					dino.duck()

			# Unduck when ducking key is released
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

			# Increase speed
			if score % 150 == 0 and score > 0:
				fps += 1

			# Incrementing score
			if frameCount % 5 == 0:
				score += 1

			frameCount += 1



main()
pygame.time.delay(750)  # Delay for player to see where they died