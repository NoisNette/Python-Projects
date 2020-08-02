import pygame, os, random

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
scissors = pygame.transform.scale(pygame.image.load('assets/scissors.png'), dims)

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
verdict = 0  # Stores the result of the game
shouldDisplayVerdict = False  # Whether to display result of game or not
incrementedScore = False  # Checker to make sure score is only incremented once per game instead of every frame


class Button:
	def __init__(self, x, y, w, h, caption=None, imgName=None, function=None, hidden=False):
		"""
		Constructor for Button class

		Args:
			x (int): x coordinate of Button
			y (int): y coordinate of Button
			w (int): width of button in pixels
			h (int): height of button in oixels
			caption (str, optional): Caption to display for Button. Defaults to None.
			imgName (str, optional): Name of image to display inside of button. Defaults to None.
			function (lambda, optional): Function to be executed if button is pressed. Defaults to None.
			hidden (bool, optional): Whether the button should be hidden upon creation. Defaults to False.
		"""
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
		"""
		Sets own image

		Args:
			imgName (str): Name of image to set

		Returns:
			pygame.Surface: Surface that represents the image
		"""
		return IMAGE_DICT.get(imgName, None)


	def draw(self, win):
		"""
		Displays self to screen

		Args:
			win (pygame.Surface): Main display surfaace
		"""
		if not self.hidden:  # Only display if button is not hidden
			if self.hovered:  # Highlight button if it is being hovered over
				pygame.draw.rect(win, LIGHT_GREY, self.rect)

			if self.function is not None:  # Draw outline if button hasn't got an image
				pygame.draw.rect(win, BLACK, self.rect, 3)

			if self.img:  # Draw image if button has it
				win.blit(self.img, (self.x, self.y))

			if self.function is not None:  # Draw caption inside button if a function is assigned to it
				font = pygame.font.Font(FONT_PATH, 30)
				label = font.render(self.caption, 1, BLACK)
				win.blit(label, (self.x + self.w // 2 - label.get_width() // 2 + 1, self.y + label.get_height() // 2 - 14))
			else:  # Draw caption under button if there is not a function assigned to it
				font = pygame.font.Font(FONT_PATH, 20)
				label = font.render(self.caption, 1, BLACK)
				win.blit(label, (self.x + self.w // 2 - label.get_width() // 2 + 1, self.y + self.h + 10))

	@property
	def hovered(self):
		"""
		Whether the button is being hovered over using the mouse

		Returns:
			bool: Result of collision checking button and mouse position
		"""
		return self.rect.collidepoint(pygame.mouse.get_pos())


	def click(self):
		"""
		Execute intended function if button is hovered and not hidden
		"""
		if self.hovered and not self.hidden:
			if self.function is not None:
				self.function()
			else:
				play(self.id)


def play(hand):
	"""
	Main logic function

	Args:
		hand (str): The hand that the player played when clicking a choice button (Rock, Paper, Scissors)
	"""
	global playerHand, computerHand, verdict, shouldDisplayVerdict
	computerHand = random.choice(CHOICES)  # Computer chooses randomly between Rock, Paper and Scissors
	playerHand = hand

	# 0 : DRAW; 1 : WIN; -1 : LOSS
	if hand == 'rock':
		verdict = 0 if computerHand == 'rock' else -1 if computerHand == 'paper' else 1
	elif hand == 'paper':
		verdict = 0 if computerHand == 'paper' else -1 if computerHand == 'scissors' else 1
	elif hand == 'scissors':
		verdict = 0 if computerHand == 'scissors' else -1 if computerHand == 'rock' else 1

	shouldDisplayVerdict = True


def displayVerdict():
	"""
	Display result of game and increment score if necessary
	"""
	global playerScore, computerScore, incrementedScore, shouldDisplayVerdict

	# Hide all buttons except Next button
	for btn in btns:
		btn.hidden = True

	nextBtn.hidden = False

	pHand = IMAGE_DICT.get(playerHand)
	cHand = IMAGE_DICT.get(computerHand)

	# Load font
	font = pygame.font.Font(FONT_PATH, 20)
	
	# Draw player's hand and caption
	pX = width // 2 - pHand.get_width() - 60
	pY = height // 2 - pHand.get_height() // 2
	win.blit(pHand, (pX, pY))
	pLabel = font.render(playerHand.capitalize(), 1, BLACK)
	win.blit(pLabel, (pX + pHand.get_width() // 2 - pLabel.get_width() // 2 + 1, pY + pHand.get_height() + 10))

	# Draw computer's hand and caption
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

	# Display verdict under hands
	font = pygame.font.Font(FONT_PATH, 32)
	label = font.render(msg, 1, BLACK)
	x = width // 2 - label.get_width() // 2
	y = height // 2 + 110
	win.blit(label, (x, y))


def returnToChoices():
	"""
	Lets the player choose his hand once again after displaying te verdict, called when Next button is pressed
	"""
	global shouldDisplayVerdict, incrementedScore

	shouldDisplayVerdict = False
	incrementedScore = False

	# Show all buttons except Next button
	for btn in btns:
		btn.hidden = False

	nextBtn.hidden = True


def draw(win):
	"""
	Draws everything to the screen

	Args:
		win (pygame.Surface): Main display surface
	"""
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
	"""
	Main game function
	"""
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
