import pygame
import os
import tkinter
from tkinter import messagebox
from tkinter import filedialog

os.system('cls')
pygame.init()
pygame.font.init()
tkinter.Tk().wm_withdraw()

width, height = 800, 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Paint')

# Load image
palette = pygame.transform.scale(pygame.image.load('palette.jpg'), (400, 300))
palette_rect = palette.get_rect()
palette_rect.x = width - palette.get_width()
palette_rect.y = 500

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (175, 175, 175)
GREY = (156, 156, 156)
FPS = 120

w = 25
h = 25
ROWS = (height - palette.get_height()) // h
COLS = width // w

# Variables
dragged = False
draw_color = BLACK
picked_color = BLACK

usingFill = False
usingEraser = False
showGrid = True

class Spot:
	"""
	Class for handling actions of a single spot
	"""
	def __init__(self, i, j):
		"""
		Constructor for Spot class

		Args:
			i (int): row index of Spot in grid
			j (int): column index of Spot in grid
		"""
		self.i = i
		self.j = j

		self.w = w
		self.h = h
		self.x = j * w
		self.y = i * h
		# Add self.rect for easier collision checking outside of class
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

		self.color = WHITE

	def draw(self, win):
		"""
		Draw self to the display

		Args:
			win (Surface): Main display surface
		"""
		pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.w))

		if showGrid:  # Only draw grid if user chooses to
			pygame.draw.rect(win, GREY, (self.x, self.y, self.w, self.w), 1)

	def fill(self, new_color, old_color):
		"""
		Function for flood-filling with a selected color

		Args:
			new_color (pygame.Color): Tuple of (int, int, int) values representing a RGB color, stores the new color that the spot needs to get
			old_color (pygame.Color): Tuple of (int, int, int) values representing a RGB color
		"""
		global grid

		# Use shorter name of variable for readability
		i = self.i
		j = self.j
		try:  # Make sure that every neighbor is possible
			if i > -1:
				if grid[i-1][j].color == old_color and grid[i-1][j].color != new_color:
					grid[i-1][j].setColor(new_color, old_color)
			if i < ROWS:
				if grid[i+1][j].color == old_color and grid[i+1][j].color != new_color:
					grid[i + 1][j].setColor(new_color, old_color)
			if j > -1:
				if grid[i][j-1].color == old_color and grid[i][j-1].color != new_color:
					grid[i][j-1].setColor(new_color, old_color)
			if j < COLS:
				if grid[i][j+1].color == old_color and grid[i][j+1].color != new_color:
					grid[i][j+1].setColor(new_color, old_color)
		except:
			return


	def setColor(self, new_color, old_color):
		"""
		Setter for setting own color and flood-filling to neighboring spots

		Args:
			new_color (pygame.Color): Tuple of (int, int, int) values representing a RGB color, stores the new color that the spot needs to get
			old_color (pygame.Color): Tuple of (int, int, int) values representing a RGB color
		"""
		self.color = new_color
		if usingFill:  # Only initiate flood-fill if user wants to fill
			self.fill(new_color, old_color)

class Button:
	"""
	Class for function buttons
	"""
	def __init__(self, x, y, w, h, caption, function, togglable=False):
		"""
		Constructor for Button class

		Args:
			x (int): x coordinate of Button
			y (int): y coordinate of Button
			w (int): width of Button
			h (int): height of Button
			caption (str): caption to be displayed on the Button
			function (lambda): function that the button needs to execute if it is pressed
			togglable (bool, optional): whether the button is a togglable switch or a button. Defaults to False.
		"""
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		# Add self.rect for easier collision checking outside of class
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

		self.caption = caption
		self.function = function
		self.togglable = togglable

		self.color = WHITE
		self.hovered = False
		self.clicked = False

	def draw(self, win):
		"""
		Draw self to the display

		Args:
			win (Surface): Main display surface
		"""
		# Check if button is hovered
		self.hover()

		# Draw button
		pygame.draw.rect(win, self.color, self.rect)
		pygame.draw.rect(win, BLACK, self.rect, 4)

		# Draw caption
		font = pygame.font.Font(None, self.w // 3)
		label = font.render(self.caption, 1, BLACK)

		# Place caption in middle of button
		x = self.x + self.w // 2 - label.get_width() // 2
		y = self.y + self.h // 2 - label.get_height() // 2
		win.blit(label, (x, y))
	
	def click(self):
		"""
		Check if button is clicked and execute function if it is
		"""
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			self.clicked = not self.clicked
			self.function()
	
	def hover(self):
		"""
		Check if button is being hovered over with the mouse and update color accordingly
		"""
		if self.togglable:  # Allow button to stay in GREY color if it is togglable
			if self.rect.collidepoint(pygame.mouse.get_pos()):  # Always set color to LIGHT_GREY if the button is hovered
				self.hovered = True
				self.color = LIGHT_GREY
			elif self.clicked:
				self.color = GREY
			else:  # Return color to default if button is not hovered or clicked
				self.hovered = False
				self.color = WHITE
		else:  # If button is not togglable
			if self.rect.collidepoint(pygame.mouse.get_pos()):
				self.hovered = True
				self.color = LIGHT_GREY
			else:  # Return color to default if button is not hovered or clicked
				self.hovered = False
				self.color = WHITE
		
		
def pickColor():
	"""
	Looks at the color of the pixel that is being clicked on

	Returns:
		pygame.Color: Tuple of (int, int, int) values representing a RGB color
	"""
	screen = pygame.display.get_surface()  # Load window surface
	mouse = pygame.mouse.get_pos()
	pxarray = pygame.PixelArray(screen)  # Load pixels
	pixel = pygame.Color(pxarray[mouse[0], mouse[1]])  # Get color of pixel at (mouseX, mouseY)

	return pixel[1:]  # Don't return alpha value

def isEmpty(grid):
	"""
	Checks if the current grid is blank

	Args:
		grid (list<list<Spot>>): Main 2d list of Spot objects

	Returns:
		bool: Whether the grid is blank
	"""
	empty_grid = [[Spot(i, j) for j in range(COLS)] for i in range(ROWS)]
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if grid[i][j].color != empty_grid[i][j].color:
				return False
	return True

def useFill():
	"""
	Function executed when Fill Button is pressed
	"""
	global usingFill
	usingFill = not usingFill

def clearScreen():
	"""
	Function executed when Clear Screen Button is pressed, resets every spot's color to WHITE
	"""
	for row in grid:
		for spot in row:
			spot.color = WHITE

def useEraser():
	"""
	Function executed when Erase Button is pressed
	"""
	global usingEraser
	usingEraser = not usingEraser

def toggleGrid():
	"""
	Function executed when Grid Button is pressed
	"""
	global showGrid
	showGrid = not showGrid

def undo():
	pass

def redo():
	pass

def saveFile():
	"""
	When Save Button is pressed, prompt user for location and name of file and create a .txt file with information about the grid
	"""
	filename = filedialog.asksaveasfilename(initialdir='./', title='Saving drawing', defaultextension='.txt', filetypes=[("Text files", "*.txt")])

	if filename:  # filename == '' if user pressed 'Cancel' in Save window
		compressed_grid = []
		for i in range(len(grid)):
			row = []
			for j in range(len(grid[i])):
				row.append(grid[i][j].color)
			compressed_grid.append(row)  # Get 2d list of colors of every spot
		
		with open(filename, 'w+') as f:  # Write to new file or overwrite existing file
			f.write(str(compressed_grid))  # All information about colors is in a single line
	else:
		return

def openFile():
	"""
	When Open Button is pressed, prompt user for location and name of file and read color information about grid, then apply to existing grid
	"""
	filename = filedialog.askopenfilename(initialdir='./', title='Opening drawing', defaultextension='.txt', filetypes=[("Text files", "*.txt")])

	if filename:  # filename == '' if user pressed 'Cancel' in Open window
		global grid
		try:  # Make sure the file is a usable file in the correct format, else popup Error dialog
			with open(filename, 'r') as f:
				lines = f.readlines()
				compressed_grid = eval(lines[0].strip())  # Only look at first line since all the data is in the first line

			for i in range(len(grid)):
				for j in range(len(grid[i])):
					grid[i][j].color = compressed_grid[i][j]  # Update current grid to saved grid
			
			name = filename.split('/')[-1]
			pygame.display.set_caption(name.split('.')[0])  # Set the name of the window to the name of the opened file
		except:
			messagebox.showinfo('Error!', 'Invalid file...')
	else:
		return

def draw(win):
	"""
	Function for drawing everything to the screen

	Args:
		win (Surface): Main display surface
	"""
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)  # Draw all spots
	
	for button in buttons:  # Draw all buttons
		button.draw(win)

	# Draw bounds
	pygame.draw.line(win, BLACK, (0, 0), (width, 0), 2)
	pygame.draw.line(win, BLACK, (0, (height - palette.get_height())), (width, (height - palette.get_height())), 2)

	# Draw color pallete
	win.blit(palette, palette_rect)

	pygame.display.update()


# Initialize grid
grid = [[Spot(i, j) for j in range(COLS)] for i in range(ROWS)]

# Initialize buttons
buttons = []

buttons.append(Button(5, 507, 75, 75, 'FILL', useFill, True))  # Fill button
buttons.append(Button(110, 507, 75, 75, 'CLEAR', clearScreen))  # Clear Screen button
buttons.append(Button(215, 507, 75, 75, 'ERASE', useEraser, True))  # Erase button

buttons.append(Button(5, 600, 75, 75, 'SAVE', saveFile))  # Save button
buttons.append(Button(110, 600, 75, 75, 'OPEN', openFile))  # Open button
buttons.append(Button(215, 600, 75, 75, 'GRID', toggleGrid))  # Toggle grid button

buttons.append(Button(5, 700, 75, 75, 'UNDO', undo))  # Undo button
buttons.append(Button(110, 700, 75, 75, 'REDO', redo))  # Redo button


def main():
	"""
	Main function for executing everything
	"""
	global dragged, draw_color, picked_color, grid, all_grids, cur_grid

	run = True
	clock = pygame.time.Clock()

	# Infinite game loop
	while run:
		clock.tick(FPS)

		# Draw window
		draw(win)

		# Set color to WHITE if user is using the Eraser tool, else return to the color they picked
		if usingEraser:
			draw_color = WHITE
		else:
			draw_color = picked_color

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				if not isEmpty(grid):
					msg = messagebox.askyesnocancel('Closing...', 'Would you like to save before closing?')
					if msg:  # Save file if 'Yes' is pressed
						saveFile()
					elif msg == False and msg is not None:  # Quit if 'No' is pressed
						quit()
					# Continue running if 'Cancel' is pressed
				else:
					quit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				# Fill spot that is being hovered over
				for row in grid:
					for spot in row:
						if spot.rect.collidepoint(pygame.mouse.get_pos()):
							if usingFill:  # Flood-fill if user is filling
								spot.fill(draw_color, spot.color)
							else:
								spot.color = draw_color  # Fill single spot

				# Call pickColor() if mouse is on color palette
				if palette_rect.collidepoint(pygame.mouse.get_pos()):
					picked_color = pickColor()
				else:
					dragged = True
				
				# Click all the buttons, checking collision with mouse is inside the click() method
				for button in buttons:
					button.click()


			elif event.type == pygame.MOUSEBUTTONUP:
				dragged = False
			
			if event.type == pygame.MOUSEMOTION and dragged:  # Fill while dragging mouse
				for row in grid:
					for spot in row:
						if spot.rect.collidepoint(pygame.mouse.get_pos()):
							if usingFill:
								spot.fill(draw_color, spot.color)
							else:
								spot.color = draw_color
		
# Call main function
main()