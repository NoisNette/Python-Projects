import pygame
import os
import random

# Initialize pygame and clear console for aesthetics
os.system('cls')
pygame.init()
pygame.font.init()

# Setup display
width, height = 800, 600
win = pygame.display.set_mode((800, 600))
pygame.display.set_caption('PONG!')

# Load sounds
clack = pygame.mixer.Sound('clack.wav')

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60
PADDLE_VEL = 4
BALL_VEL = 4

# Variables
scoreLeft = 0
scoreRight = 0


class Paddle:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.w = 25
		self.h = 120
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h) # For easier drawing and collision checking
	

	def draw(self, win):
		# Update self.rect with new coordinates, then draw
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
		pygame.draw.rect(win, WHITE, self.rect)

		# Check collision with top wall
		if self.y < 25: 
			self.y = 25

		# Check collision with bottom wall
		if self.y + self.h > height - 25:
			self.y = height - 25 - self.h
	

class Ball:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.r = 16
		self.xvel = BALL_VEL
		self.yvel = BALL_VEL
	
	def draw(self, win):
		pygame.draw.circle(win, WHITE, (self.x, self.y), self.r)

		# Update own coordinates based on the velocity
		self.x += self.xvel
		self.y += self.yvel

		# Check collision with top wall
		if self.y - self.r <= 0:
			self.yvel *= -1

		# Check collision with bottom wall
		if self.y + self.r >= height:
			self.yvel *= -1

	def collide(self, paddle):
		if paddle.x < width / 2:  # Collision with left paddle
			if paddle.rect.collidepoint(self.x - self.r, self.y):
				clack.play()
				self.x = paddle.x + paddle.w + self.r
				self.xvel *= -1	
		
		else:  # Collision with right paddle
			if paddle.rect.collidepoint(self.x + self.r, self.y):
				clack.play()
				self.x = paddle.x - self.r
				self.xvel *= -1
				

# Initialize paddles and ball
leftPaddle = Paddle(25, 250)
rightPaddle = Paddle(width - 45, 250)
ball = Ball(width // 2, height // 2)

# Function for redrawing the display
def draw(win):
	win.fill(BLACK)

	leftPaddle.draw(win)
	rightPaddle.draw(win)

	ball.draw(win)

	ball.collide(leftPaddle)
	ball.collide(rightPaddle)

	# Draw score
	score_font = pygame.font.Font('FFFFORWA.TTF', 100)
	score_label = score_font.render('{} : {}'.format(scoreLeft, scoreRight), 1, WHITE)
	win.blit(score_label, (width // 2 - score_label.get_width() // 2, 50))

	pygame.display.update()


# Function for reseting the ball to the center of the screen
def resetBall():
	ball.x = width // 2
	ball.y = height // 2
	ball.xvel = random.choice([-BALL_VEL, BALL_VEL])
	ball.yvel = random.choice([-BALL_VEL, BALL_VEL])


# Function for checking if the ball went off the screen and updating the score accordingly
def offScreen():
	global scoreLeft
	global scoreRight

	if ball.x + ball.r < 0:  # Left wall
		scoreRight += 1
		resetBall()
	
	if ball.x - ball.r > width:  # Right wall
		scoreLeft += 1
		resetBall()

def main():
	run = True
	clock = pygame.time.Clock()

	while run:
		clock.tick(FPS)

		draw(win)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()


		keys = pygame.key.get_pressed()

		if keys[pygame.K_w]:
			leftPaddle.y -= PADDLE_VEL
		
		if keys[pygame.K_s]:
			leftPaddle.y += PADDLE_VEL
		
		if keys[pygame.K_UP]:
			rightPaddle.y -= PADDLE_VEL
		
		if keys[pygame.K_DOWN]:
			rightPaddle.y += PADDLE_VEL
		
		offScreen()


def mainMenu():
	run = True
	clock = pygame.time.Clock()

	while run:
		clock.tick(FPS)

		win.fill(BLACK)
		start_font = pygame.font.Font('FFFFORWA.TTF', 40)
		start_label = start_font.render('Press any button to start...', 1, WHITE)
		win.blit(start_label, (width // 2 - start_label.get_width() // 2, height // 2 - start_label.get_height() // 2))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
			if event.type == pygame.KEYDOWN:
				main()
				run = False

		pygame.display.update()
	
mainMenu()