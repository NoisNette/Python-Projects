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
	def __init__(self, i, j):
		self.i = i
		self.j = j

		self.w = w
		self.h = h
		self.x = j * w
		self.y = i * h
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

		self.color = WHITE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.w))
		if showGrid:
			pygame.draw.rect(win, GREY, (self.x, self.y, self.w, self.w), 1)

	def fill(self, new_color, old_color):
		global grid

		i = self.i
		j = self.j
		try:
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
		self.color = new_color
		if usingFill:
			self.fill(new_color, old_color)

class Button:
	def __init__(self, x, y, w, h, caption, function, togglable=False):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

		self.caption = caption
		self.function = function
		self.togglable = togglable

		self.color = WHITE
		self.hovered = False
		self.clicked = False

	def draw(self, win):
		self.hover()

		# Draw button
		pygame.draw.rect(win, self.color, self.rect)
		pygame.draw.rect(win, BLACK, self.rect, 4)

		# Draw caption
		font = pygame.font.Font(None, self.w // 3)
		label = font.render(self.caption, 1, BLACK)

		x = self.x + self.w // 2 - label.get_width() // 2
		y = self.y + self.h // 2 - label.get_height() // 2
		win.blit(label, (x, y))
	
	def click(self):
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			self.clicked = not self.clicked
			self.function()
	
	def hover(self):
		if self.togglable:
			if self.rect.collidepoint(pygame.mouse.get_pos()):
				self.hovered = True
				self.color = LIGHT_GREY
			elif self.clicked:
				self.color = GREY
			else:
				self.hovered = False
				self.color = WHITE
		else:
			if self.rect.collidepoint(pygame.mouse.get_pos()):
				self.hovered = True
				self.color = LIGHT_GREY
			else:
				self.hovered = False
				self.color = WHITE
		
		
def pickColor():
	screen = pygame.display.get_surface()
	mouse = pygame.mouse.get_pos()
	pxarray = pygame.PixelArray(screen)
	pixel = pygame.Color(pxarray[mouse[0], mouse[1]])

	return pixel[1:]

def useFill():
	global usingFill
	usingFill = not usingFill

def clearScreen():
	for row in grid:
		for spot in row:
			spot.color = WHITE

def useEraser():
	global usingEraser
	usingEraser = not usingEraser

def toggleGrid():
	global showGrid
	showGrid = not showGrid

def saveFile():
	filename = filedialog.asksaveasfilename(initialdir='./', title='Saving drawing', defaultextension='.txt', filetypes=[("Text files", "*.txt")])

	if filename:
		compressed_grid = []
		for i in range(len(grid)):
			row = []
			for j in range(len(grid[i])):
				row.append(grid[i][j].color)
			compressed_grid.append(row)
		
		with open(filename, 'w+') as f:
			f.write(str(compressed_grid))
	else:
		return

def openFile():
	filename = filedialog.askopenfilename(initialdir='./', title='Opening drawing', defaultextension='.txt', filetypes=[("Text files", "*.txt")])

	if filename:
		global grid
		try:
			with open(filename, 'r') as f:
				lines = f.readlines()
				compressed_grid = eval(lines[0].strip())

			for i in range(len(grid)):
				for j in range(len(grid[i])):
					grid[i][j].color = compressed_grid[i][j]
			
			name = filename.split('/')[-1]
			pygame.display.set_caption(name.split('.')[0])
		except:
			messagebox.showinfo('Error!', 'Invalid file...')
	else:
		return

def draw(win):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)
	
	for button in buttons:
		button.draw(win)

	# Draw bounds
	pygame.draw.line(win, BLACK, (0, 0), (width, 0), 2)
	pygame.draw.line(win, BLACK, (0, (height - palette.get_height())), (width, (height - palette.get_height())), 2)

	win.blit(palette, palette_rect)

	pygame.display.update()


# Initialize grid
grid = [[Spot(i, j) for j in range(COLS)] for i in range(ROWS)]
old_grid = grid[:]

# Initialize buttons
buttons = []
buttons.append(Button(5, 507, 100, 100, 'FILL', useFill, True))  # Fill button
buttons.append(Button(110, 507, 100, 100, 'CLEAR', clearScreen))  # Clear screen button
buttons.append(Button(215, 507, 100, 100, 'ERASE', useEraser, True))  # Erase button

buttons.append(Button(5, 625, 100, 100, 'SAVE', saveFile))  # Save button
buttons.append(Button(110, 625, 100, 100, 'OPEN', openFile))  # Open button
buttons.append(Button(215, 625, 100, 100, 'GRID', toggleGrid))  # Toggle grid button

def main():
	global dragged, draw_color, picked_color

	run = True
	clock = pygame.time.Clock()

	while run:
		clock.tick(FPS)

		draw(win)

		if usingEraser:
			draw_color = WHITE
		else:
			draw_color = picked_color

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				msg = messagebox.askyesnocancel('Closing...', 'Would you like to save before closing?')
				if msg:
					saveFile()
				elif msg == False and msg is not None:
					quit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				# Fill spot that is being hovered over
				for row in grid:
					for spot in row:
						if spot.rect.collidepoint(pygame.mouse.get_pos()):
							if usingFill:
								spot.fill(draw_color, spot.color)
							else:
								spot.color = draw_color

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
			
			if event.type == pygame.MOUSEMOTION and dragged:
				for row in grid:
					for spot in row:
						if spot.rect.collidepoint(pygame.mouse.get_pos()):
							if usingFill:
								spot.fill(draw_color, spot.color)
							else:
								spot.color = draw_color
		

main()