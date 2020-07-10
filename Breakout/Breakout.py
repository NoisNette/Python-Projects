import pygame
import os
import math

os.system('cls')
pygame.init()
pygame.font.init()

# Setup game display
width, height = 500, 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Breakout')

# Load sound
clack = pygame.mixer.Sound('clack.wav')

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 20, 60)
ORANGE = (255, 140, 0)
GREEN = (34, 139, 34)
YELLOW = (255, 255, 0)
FPS = 60

# Variables
score = 0
lives = 3
bricks = []
gameOver = 0


class Brick:
	def __init__(self, x, y, color):
		self.x = x
		self.y = y
		self.w = 30
		self.h = 10
		self.color = color
		self.score = self.getScore()
		self.hit = False
		self.rect = None

	def delete(self):
		bricks.remove(self)

	def draw(self, win):
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
		pygame.draw.rect(win, self.color, self.rect)

	def getScore(self):
		scores = {
			RED: 7,
			ORANGE: 5,
			GREEN: 3,
			YELLOW: 1
		}
		return scores[self.color]

	def collide(self, ball):
		testX = ball.x
		testY = ball.y
		lr, tb = False, False

		if ball.x < self.x:  # Left edge
			testX = self.x
			lr = True

		elif ball.x > self.x + self.w:  # Right edge
			testX = self.x + self.w
			lr = True

		if ball.y < self.y:  # Top edge
			testY = self.y
			tb = True

		elif ball.y > self.y + self.h:  # Bottom edge
			testY = self.y + self.h
			tb = True

		distX = ball.x - testX
		distY = ball.y - testY
		dist = math.sqrt(distX ** 2 + distY ** 2)

		if dist <= ball.r:
			global score
			score += self.score

			if lr:
				ball.xvel *= -1
			elif tb:
				ball.yvel *= -1
			return True

		return False


class Ball:
	def __init__(self):
		self.x = width // 2
		self.y = height - 100
		self.r = 10
		self.xvel = 3
		self.yvel = -3
		self.rect = None
		self.dead = True

	def draw(self, win):
		rect = pygame.draw.circle(win, WHITE, (self.x, self.y), self.r)
		self.rect = rect

		if not self.dead:
			self.x += self.xvel
			self.y += self.yvel

		if self.x - self.r < 0:  # Left wall
			self.xvel *= -1
			clack.play()

		if self.x + self.r > width:  # Right wall
			self.xvel *= -1
			clack.play()

		if self.y - self.r < 0:  # Top wall
			self.yvel *= -1
			clack.play()

		if self.collidePaddle():  # Paddle
			self.yvel *= -1
			clack.play()

		if ball.y - ball.r >= height:  # Offscreen
			global lives
			lives -= 1
			self.resetBall()

	def collidePaddle(self):
		if paddle.rect.collidepoint(self.x, self.y + self.r):
			if self.y + self.r > paddle.x:
				self.y -= 3
				clack.play()
				return True
		return False

	def resetBall(self):
		self.x = width // 2
		self.y = height - 100
		self.xvel = abs(self.xvel)
		self.yvel = -abs(self.yvel)
		self.dead = True


class Paddle:
	def __init__(self):
		self.x = 190
		self.y = height - 40
		self.w = 120
		self.h = 20
		self.vel = 3
		self.rect = None

	def draw(self, win):
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
		pygame.draw.rect(win, WHITE, self.rect)

		if self.x <= 10:
			self.x = 10
		if self.x + self.w >= width - 10:
			self.x = width - 10 - self.w


def draw(win):
	win.fill(BLACK)

	for brick in bricks[:]:
		brick.draw(win)
		if brick.collide(ball):
			clack.play()
			brick.delete()

	paddle.draw(win)

	ball.draw(win)

	# Draw lives and score
	livesScore_font = pygame.font.Font('FFFFORWA.TTF', 24)

	lives_label = livesScore_font.render('Lives: {}'.format(lives), 1, WHITE)
	score_label = livesScore_font.render('Score: {}'.format(score), 1, WHITE)

	win.blit(lives_label, (10, 10))
	win.blit(score_label, (width - score_label.get_width() - 10, 10))

	pygame.display.update()


# Initialize bricks
for i in range(20):  # Red bricks
	x = 30 + (i % 10) * 45
	y = 100 + 20 * (i // 10)
	brick = Brick(x, y, RED)
	bricks.append(brick)

for i in range(20):  # Orange bricks
	x = 30 + (i % 10) * 45
	y = 140 + 20 * (i // 10)
	brick = Brick(x, y, ORANGE)
	bricks.append(brick)

for i in range(20):  # Green bricks
	x = 30 + (i % 10) * 45
	y = 180 + 20 * (i // 10)
	brick = Brick(x, y, GREEN)
	bricks.append(brick)

for i in range(20):  # Yellow bricks
	x = 30 + (i % 10) * 45
	y = 220 + 20 * (i // 10)
	brick = Brick(x, y, YELLOW)
	bricks.append(brick)

# Initialize ball
ball = Ball()

# Initialize paddle
paddle = Paddle()


def main():
	global gameOver
	global lives

	run = True
	clock = pygame.time.Clock()

	while run:
		clock.tick(FPS)

		if gameOver == -1:  # Loss
			win.fill(BLACK)

			end_font = pygame.font.Font('FFFFORWA.TTF', 32)

			lost_label = end_font.render('GAME OVER!', 1, WHITE)
			score_label = end_font.render('SCORE: {}'.format(score), 1, WHITE)

			win.blit(lost_label, (width // 2 - lost_label.get_width() // 2, 200))
			win.blit(score_label, (width // 2 - score_label.get_width() // 2, 500))

			pygame.display.update()

		if gameOver == 1:  # Victory
			win.fill(BLACK)

			end_font = pygame.font.Font('FFFFORWA.TTF', 32)

			lost_label = end_font.render('VICTORY!', 1, WHITE)
			score_label = end_font.render('SCORE: {}'.format(score), 1, WHITE)

			win.blit(lost_label, (width // 2 - lost_label.get_width() // 2, 200))
			win.blit(score_label, (width // 2 - score_label.get_width() // 2, 500))

			pygame.display.update()
		else:  # Default
			draw(win)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

		keys = pygame.key.get_pressed()

		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			paddle.x -= paddle.vel
		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			paddle.x += paddle.vel

		if ball.dead:
			if keys[pygame.K_SPACE]:
				ball.dead = False

		if len(bricks) == 0:
			gameOver = 1

		elif lives == 0:
			gameOver = -1


main()
