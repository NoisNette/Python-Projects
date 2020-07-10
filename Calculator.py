import pygame
import os

# Initialize pygame and clear console for aesthetics
os.system('cls')
pygame.init()
pygame.font.init()

# Setup game window
width, height = 600, 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Calculator')

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (25, 25, 25)
LIGHT_GREY = (75, 75, 75)
ORANGE = (255, 140, 0)
DARK_ORANGE = (225, 110, 0)
SYMBOLS = [
	['<=', 'c', 'x', '/'],
	['7', '8', '9', '-'],
	['4', '5', '6', '+'],
	['1', '2', '3'], # = ],
	['Ans', '0', '.'] # = ]
]
OPERATORS = ['+', '-', '/', 'x']

# Variables
btnW = width // 4 - 3
btnH = height // 6 - 3
buttons = []
equation = ''
answer = ''
error = False

# Function for drawing everything to the screen
def draw(win):
	win.fill(DARK_GREY)

	# Draw buttons
	for btn in buttons:
		btn.draw(win)
	
	# Draw input / output box and text
	pygame.draw.rect(win, BLACK, (6, 6, width - 15, btnH + 10))

	io_font = pygame.font.SysFont('default', 85)

	if error: # Display 'ERROR' if error present
		io_label = io_font.render('ERROR', 1, WHITE)
	else:
		io_label = io_font.render(equation, 1, WHITE) # Display equation

	win.blit(io_label, (width - io_label.get_width() - 15, btnH // 2))

	pygame.display.update()

class Button:
	def __init__(self, x, y, w, h, symbol):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.symbol = symbol
		self.hovered = False
		self.color = None
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
	
	# Draw own box and symbol
	def draw(self, win):
		if self.symbol == '=': # 'Equals'(=) Button is differently colored
			if self.hover():
				self.color = DARK_ORANGE
			else:
				self.color = ORANGE
		else: # Default coloring for all Buttons except 'Equals'
			if self.hover():
				self.color = LIGHT_GREY
			else:
				self.color = BLACK
		
		pygame.draw.rect(win, self.color, self.rect) # Draw Button's box

		symbol_font = pygame.font.SysFont('default', 85)
		symbol_label = symbol_font.render(self.symbol, 1, WHITE) # Display Button's symbol
		labelX = self.x + self.w // 2 - symbol_label.get_width() // 2
		labelY = self.y + self.h // 2 - symbol_label.get_height() // 2 + 2

		win.blit(symbol_label, (labelX, labelY))

	# Check if mouse is hovering on top of Button
	def hover(self):
		if self.rect.collidepoint(pygame.mouse.get_pos()): # Check if mouse is on the box
			self.hovered = True
			return True
		else:
			self.hovered = False
			return False
	
	# Handling input and output, error checking
	def click(self):
		global equation
		global answer
		global error

		if self.hovered: # Only click Buttons that are being hovered over
			if self.symbol not in ['Ans', '=', 'c', '<=']: # Special keys that have different functions
				if self.symbol in OPERATORS: # Add padding if self.symbol is an operator
					if len(equation) + 3 <= 16:
						equation += ' ' + self.symbol + ' '
				elif len(equation) + 1 <= 16: # Make sure not to run out of space on display if the number is too long
					equation += self.symbol

			if self.symbol == '=':
				try: # Checking for division by zero
					answer = str(round(eval(equation.replace('x', '*')), 2)) # Replacing 'x' with '*' and evaluating the equation
				except:
					error = True # Set error variable to True if error present
				equation = str(answer)

			if self.symbol == 'Ans': # Add the latest answer to the equation
				equation += str(answer)

			if self.symbol == 'c': # Reset all values
				equation = ''
				answer = ''
				error = False

			if self.symbol == '<=': # Delete last character in equation
				equation = equation[:-1]

			for op in OPERATORS: # Add answer to start of equation if equation starts with an operator
				if equation.startswith(op): equation = str(answer) + equation


# Initialize buttons
for i, row in enumerate(SYMBOLS):
	for j, symbol in enumerate(row):
		x = 6 + j * btnW
		y = btnH + 20 + i * btnH
		btn = Button(x, y, btnW - 3, btnH - 3, symbol)
		buttons.append(btn)
equals = Button(448, 473, btnW - 5, btnH * 2 - 5, '=')
buttons.append(equals)


# Game loop and setup
FPS = 60
run = True
clock = pygame.time.Clock()

while run:
	clock.tick(FPS)

	draw(win)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			for btn in buttons:
				btn.click()