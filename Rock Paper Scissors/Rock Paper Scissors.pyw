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

IMAGE_DICT = {
	'rock': rock,
	'paper': paper,
	'scissors': scissors
}

# Variables
playerScore = 0
computerScore = 0
playerHand = None
computerHand = None
verdict = 0
shouldDisplayVerdict = False
incrementedScore = False


class Button:
	def __init__(self, x, y, w, h, caption=None, imgName=None, function=None, hidden=False):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

		self.caption = caption
		self.img = self.setImage(imgName)
		self.id = self.caption.lower()

		self.function = function

		self.hidden = hidden


	def setImage(self, imgName):
		return IMAGE_DICT.get(imgName, None)


	def draw(self, win):
		if not self.hidden:
			if self.hovered:
				pygame.draw.rect(win, LIGHT_GREY, self.rect)

			if self.function is not None:
				pygame.draw.rect(win, BLACK, self.rect, 3)

			if self.img:
				win.blit(self.img, (self.x, self.y))

			if self.function is not None:
				font = pygame.font.Font(FONT_PATH, 30)
				label = font.render(self.caption, 1, BLACK)
				win.blit(label, (self.x + self.w // 2 - label.get_width() // 2 + 1, self.y + label.get_height() // 2 - 14))
			else:
				font = pygame.font.Font(FONT_PATH, 20)
				label = font.render(self.caption, 1, BLACK)
				win.blit(label, (self.x + self.w // 2 - label.get_width() // 2 + 1, self.y + self.h + 10))

	@property
	def hovered(self):
		return self.rect.collidepoint(pygame.mouse.get_pos())


	def click(self):
		if self.hovered and not self.hidden:
			if self.function is not None:
				self.function()
			else:
				play(self.id)


def play(hand):
	global playerHand, computerHand, verdict, shouldDisplayVerdict
	computerHand = random.choice(CHOICES)
	playerHand = hand

	if hand == 'rock':
		verdict = 0 if computerHand == 'rock' else -1 if computerHand == 'paper' else 1
	elif hand == 'paper':
		verdict = 0 if computerHand == 'paper' else -1 if computerHand == 'scissors' else 1
	elif hand == 'scissors':
		verdict = 0 if computerHand == 'scissors' else -1 if computerHand == 'rock' else 1

	shouldDisplayVerdict = True


def displayVerdict():
	global playerScore, computerScore, incrementedScore, shouldDisplayVerdict

	for btn in btns:
		btn.hidden = True

	nextBtn.hidden = False

	pHand = IMAGE_DICT.get(playerHand)
	cHand = IMAGE_DICT.get(computerHand)

	# Load font
	font = pygame.font.Font(FONT_PATH, 20)
	
	# Draw player's hand
	pX = width // 2 - pHand.get_width() - 60
	pY = height // 2 - pHand.get_height() // 2
	win.blit(pHand, (pX, pY))
	pLabel = font.render(playerHand.capitalize(), 1, BLACK)
	win.blit(pLabel, (pX + pHand.get_width() // 2 - pLabel.get_width() // 2 + 1, pY + pHand.get_height() + 10))

	# Draw computer's hand
	cX = width // 2 + 60
	cY = height // 2 - cHand.get_height() // 2
	win.blit(cHand, (cX, cY))
	cLabel = font.render(computerHand.capitalize(), 1, BLACK)
	win.blit(cLabel, (cX + cHand.get_width() // 2 - cLabel.get_width() // 2 + 1, cY + cHand.get_height() + 10))

	if verdict == 0:
		msg = 'DRAW!'

	elif verdict == 1:
		msg = 'YOU WIN!'
		if not incrementedScore:
			playerScore += 1
			incrementedScore = True

	elif verdict == -1:
		msg = 'YOU LOSE!'
		if not incrementedScore:
			computerScore += 1
			incrementedScore = True

	font = pygame.font.Font(FONT_PATH, 32)
	label = font.render(msg, 1, BLACK)
	x = width // 2 - label.get_width() // 2
	y = height // 2 + 110
	win.blit(label, (x, y))


def returnToChoices():
	global shouldDisplayVerdict, incrementedScore

	shouldDisplayVerdict = False
	incrementedScore = False

	for btn in btns:
		btn.hidden = False

	nextBtn.hidden = True


def draw(win):
	win.fill(WHITE)

	# Display title
	font = pygame.font.Font(FONT_PATH, 40)
	label = font.render('Rock Paper Scissors', 1, BLACK)
	win.blit(label, (width // 2 - label.get_width() // 2, 55))

	# Display score
	font = pygame.font.Font(FONT_PATH, 24)
	text = 'Player {} : {} Computer'.format(playerScore, computerScore)
	label = font.render(text, 1, BLACK)
	win.blit(label, (width // 2 - label.get_width() // 2, 155))

	# Display buttons
	for btn in btns:
		btn.draw(win)

	if shouldDisplayVerdict:
		displayVerdict()

	pygame.display.update()


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
		

# Objects
rock = Button(100, 230, 100, 100, 'Rock', 'rock')
paper = Button(250, 230, 100, 100, 'Paper', 'paper')
scissors = Button(400, 230, 100, 100, 'Scissors', 'scissors')
nextBtn = Button(200, 500, 200, 50, 'Continue', function=returnToChoices, hidden=True)

btns = [rock, paper, scissors, nextBtn]


main()
