import pygame
import random
import os

os.system('cls')
pygame.init()
pygame.font.init()

# Setup game display
width, height = 800, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FPS = 60

# Variables
pipes = []
frameCount = 0
score = 0


class Bird:
	def __init__(self, x, y):
		"""
		Constructor for Bird

		Args:
			x (int): x coordinate of center of bird
			y (int): y coordinate of center of bird
		"""
		self.x = x
		self.y = y
		self.r = 16
		self.vel = 0
		self.grav = 0.8
		self.lift = -20

	def draw(self, win):
		"""
		Display bird on screen, move it and make sure it's on the screen

		Args:
			win (Surface): Main display surface
		"""
		pygame.draw.circle(win, WHITE, (self.x, self.y), self.r)

		self.vel += self.grav
		self.vel = round(self.vel * 0.95)
		self.y += self.vel

		if self.y - self.r < 0:
			self.y = self.r
			self.vel = 0

		if self.y + self.r > height:
			self.y = height - self.r
			self.vel = 0

	def flap(self):
		"""
		Flap bird every time SPACE is pressed
		"""
		self.vel += self.lift
		self.vel = max(self.vel, -17)


class Pipe:
	def __init__(self, x):
		"""
		Constructor for pipes

		Args:
			x (int): starting x coordinate of pipe
		"""
		self.x = x
		self.top = random.randint(50, 250)
		self.bot = self.top + 100
		self.vel = 3
		self.w = 20
		self.topRect = None
		self.botRect = None
		self.highlight = False
		self.passed = False
		self.hit = False

	def draw(self, win):
		"""
		Display and move pipe on screen

		Args:
			win (Surface): Main display surface
		"""
		self.topRect = pygame.Rect(self.x, 0, self.w, self.top)
		self.botRect = pygame.Rect(self.x, self.bot, self.w, height - self.bot)

		if self.highlight:
			color = RED
		else:
			color = WHITE

		self.x -= self.vel

		pygame.draw.rect(win, color, self.topRect)
		pygame.draw.rect(win, color, self.botRect)

	def offscreen(self):
		"""
		Remove pipe from pipes list if it is offscreen
		"""
		if self.x + self.w < 0:
			pipes.remove(self)

	def collide(self, bird):
		"""
		Check for collision between pipe and bird

		Args:
			bird (Bird): Bird object

		Returns:
			bool: Whether pipe and bird are colliding
		"""
		if bird.y <= self.top or bird.y >= height - self.bot:
			if bird.x >= self.x and bird.x <= self.x + self.w:
				self.highlight = True
				self.hit = True
				return True

		self.highlight = False
		return False


def draw(win):
	"""
	Draw everything to the screen

	Args:
		win (Surface): Main display surface
	"""
	global score

	win.fill(BLACK)

	for pipe in pipes[:]:
		pipe.draw(win)

		pipe.collide(bird)

		if bird.x >= pipe.x + pipe.w and not pipe.passed:
			if not pipe.hit:
				pipe.passed = True
				score += 1

		pipe.offscreen()

	bird.draw(win)

	font = pygame.font.Font(None, 48)
	label = font.render('SCORE: {}'.format(score), 1, WHITE)
	win.blit(label, (10, 10))

	pygame.display.update()


# Initialize bird
bird = Bird(100, height // 2)


def main():
	"""
	Main function with game loop
	"""
	global frameCount
	clock = pygame.time.Clock()
	run = True

	while run:
		clock.tick(FPS)

		draw(win)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.KEYDOWN:
				if event.unicode == ' ':
					bird.flap()

		if frameCount % 100 == 0:
			pipes.append(Pipe(width))

		frameCount += 1


main()
