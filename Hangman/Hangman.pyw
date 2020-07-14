import pygame
import os
import random
import string
import math

os.system('cls')

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Setup display
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Hangman')

# Load images
checkmark = pygame.transform.scale(
	pygame.image.load('checkmark.png'), (32, 32))
images = []
for i in range(7):
	image = pygame.image.load('hangman' + str(i) + '.png')
	images.append(image)

# Load sounds
right = pygame.mixer.Sound('right.wav')
wrong = pygame.mixer.Sound('wrong.wav')
victory = pygame.mixer.Sound('victory.wav')
lost = pygame.mixer.Sound('lost.wav')


# Function for loading list of words from words file
def getWords():
	global wordChoice

	# Choose correct words file depending on language choice
	if wordChoice == 0:
		words = 'wordsEN.txt'
	elif wordChoice == 1:
		words = 'wordsHR.txt'

	with open(words, 'r') as f:
		lines = f.readlines()

	# Remove '\n' from each line
	lines = [line[:-1] for line in lines[:-1]] + [lines[-1]]

	return lines


# Define variables
hangmanIndex = 0
LETTERS = list(string.ascii_uppercase)
buttons = []
letters = []
wordChoice = 0
WORDS = getWords()
WORD = random.choice(WORDS).upper()
won = False
lose = False

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (150, 150, 150)
DARK_GREY = (100, 100, 100)


class Button:
	def __init__(self, x, y, letter):
		self.x = x
		self.y = y
		self.r = 28
		self.letter = letter
		self.clicked = False
		self.hovered = False

	# Draw own circle and letter
	def draw(self, win):
		if not self.clicked:  # Draw only if not already clicked
			if self.isHovered(pygame.mouse.get_pos()):  # Change color if hovered
				color = DARK_GREY
			else:
				color = LIGHT_GREY

			pygame.draw.circle(win, color, (self.x, self.y), self.r)  # Draw circle
			pygame.draw.circle(win, BLACK, (self.x, self.y),
			                   self.r, 2)  # Draw bounding circle

			letter_font = pygame.font.Font(None, self.r * 2)

			letter_label = letter_font.render(self.letter, 1, WHITE)
			letterW, letterH = letter_label.get_width(), letter_label.get_height()

			win.blit(letter_label, (self.x - letterW // 2, self.y - letterH // 2))

	# Function for checking if the button is being hovered over or not
	def isHovered(self, mousePos):
		mouseX, mouseY = mousePos
		dist = math.sqrt((self.x - mouseX)**2 + (self.y - mouseY)**2)
		if dist <= self.r:
			self.hovered = True
			return True
		self.hovered = False
		return False

	# Function for checking if the button's been clicked and playing the game
	def click(self):
		if not self.clicked:
			if self.hovered:  # The button can only be clicked if it was first hovered over
				self.clicked = True
			if self.letter not in WORD:  # Wrong letter picked
				wrong.play()  # Play wrong sound effect
				global hangmanIndex
				hangmanIndex += 1  # Increment hangman image index and make sure it's less than 7
				if hangmanIndex == 7:
					hangmanIndex = 6
			else:  # Correct letter picked
				right.play()  # Play right sound effect
				for letter in letters:
					if letter.letter == self.letter:  # Show every correct letter in the word
						letter.found = True


class Letter:
	def __init__(self, x, y, letter):
		self.x = x
		self.y = y
		self.letter = letter
		self.found = False

	# Function for drawing own letter or underscore
	def draw(self, win):
		if not self.found:  # Draw underscore ('_') if letter not found
			letter_label = pygame.font.Font(None, 86)
			letter = letter_label.render('_', 1, BLACK)
			win.blit(letter, (self.x, self.y - 65))
		else:  # Draw own letter if letter found
			letter_label = pygame.font.Font(None, 64)
			letter = letter_label.render(self.letter, 1, BLACK)
			win.blit(letter, (self.x, self.y - 50))


class MenuButton:
	def __init__(self, x, y, w, h, caption):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.caption = caption
		self.color = LIGHT_GREY
		self.font_color = BLACK
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
		self.hovered = False

	# Function for drawing button and button's text
	def draw(self, win):
		# Change color if button is hovered
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			self.hovered = True
			self.color = DARK_GREY
			self.font_color = WHITE
		else:
			self.hovered = False
			self.color = LIGHT_GREY
			self.font_color = BLACK

		pygame.draw.rect(win, self.color, self.rect)  # Draw button's rectangle
		pygame.draw.rect(win, BLACK, self.rect, 1)  # Draw button's bounding box

		font = pygame.font.Font(None, 32)
		label = font.render(self.caption, 1, self.font_color)

		x = self.x + self.w // 2 - label.get_width() // 2
		y = self.y + self.h // 2 - label.get_height() // 2
		win.blit(label, (x, y))  # Draw button's caption

	# Function for executing a specific function if button has been pressed
	def click(self):
		global wordChoice
		if self.hovered:  # Button can only be pressed if it was previously being hovered over
			if self.caption == 'EN':  # Set language to English if 'EN' button is pressed
				wordChoice = 0

			elif self.caption == 'HR':  # Set language to Croatian if 'HR' button is pressed
				wordChoice = 1

			elif self.caption == 'PLAY':  # Start main function if 'PLAY' button is pressed
				main()


# Initialize buttons
for i in range(13):  # First row of buttons
	button = Button(38 + i * 60, 375, LETTERS[i])
	buttons.append(button)
for i in range(13):  # Second row of buttons
	button = Button(38 + i * 60, 450, LETTERS[i + 13])
	buttons.append(button)

# Initialize letters
for i in range(len(WORD)):
	letter = Letter(375 + i * 50, 250, WORD[i])
	letters.append(letter)

# Initialize menu buttons
eng = MenuButton(150, 175, 150, 150, 'EN')
hrv = MenuButton(500, 175, 150, 150, 'HR')
play = MenuButton(325, 400, 150, 75, 'PLAY')

# Function for drawing main menu


def drawMenu(win):
	# Draw background
	win.fill(WHITE)

	# Draw all buttons
	eng.draw(win)
	hrv.draw(win)
	play.draw(win)

	font = pygame.font.Font(None, 100)
	label = font.render('HANGMAN', 1, BLACK)
	win.blit(label, (WIDTH // 2 - label.get_width() // 2, 20))  # Draw game title

	# Choosing coordinates of checkmark under the chosen language's button
	if wordChoice == 0:
		x = eng.x + eng.w // 2 - checkmark.get_width() // 2
		y = eng.y + eng.h + 5

	elif wordChoice == 1:
		x = hrv.x + hrv.w // 2 - checkmark.get_width() // 2
		y = hrv.y + hrv.h + 5

	win.blit(checkmark, (x, y))  # Drawing checkmark at chosen coordinates

# Main function for running the game


def main():
	global won
	global lose

	FPS = 60
	clock = pygame.time.Clock()
	run = True

	# Main game loop
	while run:
		clock.tick(FPS)
		os.system('cls')

		# Draw background and hangman image
		win.fill(WHITE)
		win.blit(images[hangmanIndex], (150, 100))

		# Draw every button and every letter
		for button in buttons:
			button.draw(win)
		for letter in letters:
			letter.draw(win)

		# End the game if the game is over
		if won or lose:
			run = False

		# Event loop
		for event in pygame.event.get():
			if event.type == pygame.QUIT:  # Quit if user quits
				quit()

			# Checking for clicking buttons
			if event.type == pygame.MOUSEBUTTONDOWN:
				for button in buttons:
					if button.hovered:
						button.click()

		# Displaying lose message if game is lost
		if hangmanIndex == 6:
			lost_label = pygame.font.Font(None, 70)
			label = lost_label.render('YOU LOST!', 1, BLACK)

			win.blit(label, (WIDTH // 2 - label.get_width() // 2, 10))
			lose = True

			# Uncover entire word
			for letter in letters:
				letter.found = True

		# Check if all letters have been found, if so display win message
		elif all(letter.found for letter in letters):
			won_label = pygame.font.Font(None, 70)
			label = won_label.render('YOU WON!', 1, BLACK)

			win.blit(label, (WIDTH // 2 - label.get_width() // 2, 10))
			won = True

		pygame.display.update()

	pygame.time.delay(1750)

# Function for displaying the main menu


def mainMenu():
	FPS = 60
	clock = pygame.time.Clock()
	run = True

	# Main menu loop
	while run:
		clock.tick(FPS)
		os.system('cls')

		# Draw menu
		drawMenu(win)

		# Event loop
		for event in pygame.event.get():
			if event.type == pygame.QUIT:  # Quit if user quits
				quit()

			# Check for clicking buttons
			if event.type == pygame.MOUSEBUTTONDOWN:
				eng.click()
				hrv.click()
				play.click()

		pygame.display.update()


mainMenu()

# Delay to allow right or wrong sound to be played to the end
pygame.time.delay(500)
if won:  # Play victory sound if player won
	victory.play()
elif lose:  # Play loss sound if player lost
	lost.play()
# Wait for sound to finish playing and player to see entire word
pygame.time.delay(1750)
pygame.quit()
quit()  # Quit the program
