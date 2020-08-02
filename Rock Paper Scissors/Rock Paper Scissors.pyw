import pygame
import os
import random


os.system('cls')
pygame.init()
pygame.font.init()

# Setup game display
width, height = 600, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Rock Paper Scissors')
pygame.display.set_icon(pygame.image.load('assets/icon.png'))

# Load images
dims = (100, 100)
rock = pygame.transform.scale(pygame.image.load('assets/rock.png'), dims)
paper = pygame.transform.scale(pygame.image.load('assets/paper.png'), dims)
scissors = pygame.transform.scale(
	pygame.image.load('assets/scissors.png'), dims)

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (235, 235, 235)
FPS = 60
FONT_PATH = 'assets/Montserrat.ttf'
clock = pygame.time.Clock()
CHOICES = ['rock', 'paper', 'scissors']

# Variables
playerScore = 0
computerScore = 0
playerHand = None
computerHand = None
verdict = 0


class Button:
	def __init__(self, x, y, w, h, caption=None, imgName=None):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

		self.caption = caption
		self.img = self.setImage(imgName)
		self.id = self.caption.lower()

		self.hovered = False
		self.hidden = False


	def setImage(self, imgName):
		if imgName:
			if imgName == 'rock':
				return rock
			elif imgName == 'paper':
				return paper
			elif imgName == 'scissors':
				return scissors
		return None


	def draw(self, win):
		if not self.hidden:
			self.hover()

			if self.hovered:
				pygame.draw.rect(win, LIGHT_GREY, self.rect)

			if self.img:
				win.blit(self.img, (self.x, self.y))

			font = pygame.font.Font(FONT_PATH, 20)
			label = font.render(self.caption, 1, BLACK)
			win.blit(label, (self.x + self.w // 2 -
                            label.get_width() // 2, self.y + self.h + 10))


	def hover(self):
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			self.hovered = True
		else:
			self.hovered = False

	def click(self):
		if self.hovered and not self.hidden:
			play(self.id)


# Objects
rock = Button(100, 300, 100, 100, 'Rock', 'rock')
paper = Button(250, 300, 100, 100, 'Paper', 'paper')
scissors = Button(400, 300, 100, 100, 'Scissors', 'scissors')

btns = [rock, paper, scissors]


def draw(win):
	win.fill(WHITE)

	# Display title
	font = pygame.font.Font(FONT_PATH, 40)
	label = font.render('Rock Paper Scissors', 1, BLACK)
	win.blit(label, (width // 2 - label.get_width() // 2, 75))

	# Display score
	font = pygame.font.Font(FONT_PATH, 24)
	text = 'Player {} : {} Computer'.format(playerScore, computerScore)
	label = font.render(text, 1, BLACK)
	win.blit(label, (width // 2 - label.get_width() // 2, 175))

	# Display buttons
	for btn in btns:
		btn.draw(win)

	pygame.display.update()


def play(hand):
	global playerHand, computerHand, verdict
	computerHand = random.choice(CHOICES)
	if hand == 'rock':
		verdict = 0 if computerHand == 'rock' else -1 if computerHand == 'paper' else 1
	elif hand == 'paper':
		verdict = 0 if computerHand == 'paper' else - \
			1 if computerHand == 'scissors' else 1
	elif hand == 'scissors':
		verdict = 0 if computerHand == 'scissors' else -1 if computerHand == 'rock' else 1


def main():
	run = True
	while run:
		clock.tick(FPS)

		draw(win)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				for btn in btns:
					btn.click()


main()
