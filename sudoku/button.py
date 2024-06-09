import pygame

from config import *

class Button:
	def __init__(self, text, x, y, w, h, command):
		self.text = text

		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.rect = pygame.Rect(x, y, w, h)

		self.command = command

		self.font = pygame.font.Font(None, CELL_SIZE//2)

	@property
	def isHovered(self):
		return self.rect.collidepoint(pygame.mouse.get_pos())

	def click(self):
		if self.isHovered:
			self.command()
		
	def draw(self, win):
		backgroundColor = MATCHING_ROW_COL_QUAD if self.isHovered else WHITE

		pygame.draw.rect(
			win,
			backgroundColor,
			self.rect,
			border_radius=10
		)
		pygame.draw.rect(
			win,
			BLACK,
			self.rect,
			3,
			border_radius=10
		)

		textLabel = self.font.render(self.text, 1, MATCHING_NUMBER)
		x = self.x+self.w//2 - textLabel.get_width()//2
		win.blit(textLabel, (x, self.y+self.h+5))

class ToggleButton(Button):
	def __init__(self, *args):
		super().__init__(*args)
		self.isToggled = False
		self.toggledFont = pygame.font.Font(None, self.w)

	def click(self):
		self.isToggled = not self.isToggled
		self.command()

	def draw(self, win):
		backgroundColor = MATCHING_ROW_COL_QUAD if self.isHovered else WHITE

		pygame.draw.rect(
			win,
			backgroundColor,
			self.rect,
			border_radius=10
		)
		pygame.draw.rect(
			win,
			BLACK,
			self.rect,
			3,
			border_radius=10
		)

		textLabel = self.font.render(self.text, 1, MATCHING_NUMBER)
		win.blit(textLabel, (self.x+self.w//2-textLabel.get_width()//2, self.y+self.h+5))

		if self.isToggled:
			xLabel = self.toggledFont.render('X', 1, BLACK)
			x = self.x+self.w//2 - xLabel.get_width()//2
			y = self.y+self.h//2 - xLabel.get_height()//2
			win.blit(xLabel, (x-1, y+1))

class NumButton(Button):
	def __init__(self, *args):
		super().__init__(*args)
		self.font = pygame.font.Font(None, CELL_SIZE)
		self.isDisabled = False

	@property
	def isHovered(self):
		return (not self.isDisabled) and self.rect.collidepoint(pygame.mouse.get_pos())

	def disable(self):
		self.isDisabled = True

	def draw(self, win):
		if self.isDisabled:
			return

		backgroundColor = MATCHING_ROW_COL_QUAD if self.isHovered else WHITE

		pygame.draw.rect(
			win,
			backgroundColor,
			self.rect,
			border_radius=10
		)
		pygame.draw.rect(
			win,
			BLACK,
			self.rect,
			3,
			border_radius=10
		)

		numLabel = self.font.render(self.text, 1, BLACK)
		x = self.x+self.w//2 - numLabel.get_width()//2
		y = self.y+self.h//2 - numLabel.get_height()//2
		win.blit(numLabel, (x-1, y+1))