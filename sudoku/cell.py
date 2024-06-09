import pygame

from config import *

class Cell:
	def __init__(self, i, j, xOff, yOff, num, correctNum, isEditable):
		self.i = i
		self.j = j
		self.num = num
		self.correctNum = correctNum

		self.quadrant = (i // 3) * 3 + (j // 3)

		self.x = xOff + self.j*CELL_SIZE
		self.y = yOff + self.i*CELL_SIZE

		self.isEditable = isEditable
		self.isWrong = False

		self.notes = []

		self.numberFont = pygame.font.Font(None, CELL_SIZE)
		self.noteFont = pygame.font.Font(None, CELL_SIZE//3)

	def set(self, num, correctNum, editable):
		self.num = num
		self.correctNum = correctNum
		self.isEditable = editable
		self.isWrong = False

	def collides(self, x, y):
		return (self.x <= x <= self.x+CELL_SIZE) and \
			   (self.y <= y <= self.y+CELL_SIZE)

	def mark(self, num):
		self.num = num

		if self.num == self.correctNum:
			self.isEditable = False
			self.isWrong = False
		else:
			self.isWrong = True

	def erase(self):
		if self.isEditable:
			self.num = 0
			self.isWrong = False

	def draw(self, win, selectedNumber, selectedI, selectedJ, selectedQuadrant):
		backgroundColor = SELECTED_CELL if (selectedI == self.i and selectedJ == self.j) else MATCHING_NUMBER if self.num == selectedNumber else MATCHING_ROW_COL_QUAD if (selectedI == self.i or selectedJ == self.j or selectedQuadrant == self.quadrant) else WHITE

		topBorder = BLACK if self.i % 3 == 0 else MATCHING_NUMBER
		leftBorder = BLACK if self.j % 3 == 0 else MATCHING_NUMBER
		bottomBorder = BLACK if self.i % 3 == 2 else MATCHING_NUMBER
		rightBorder = BLACK if self.j % 3 == 2 else MATCHING_NUMBER

		pygame.draw.rect(
			win,
			backgroundColor,
			(
				self.x,
				self.y,
				CELL_SIZE,
				CELL_SIZE
			)
		)
		pygame.draw.line(win, topBorder, (self.x, self.y), (self.x+CELL_SIZE, self.y), 1 if self.i % 3 != 0 else 2)
		pygame.draw.line(win, leftBorder, (self.x, self.y), (self.x, self.y+CELL_SIZE), 1 if self.j % 3 != 0 else 2)
		pygame.draw.line(win, bottomBorder, (self.x, self.y+CELL_SIZE), (self.x+CELL_SIZE, self.y+CELL_SIZE), 1 if self.i % 3 != 2 else 2)
		pygame.draw.line(win, rightBorder, (self.x+CELL_SIZE, self.y), (self.x+CELL_SIZE, self.y+CELL_SIZE), 1 if self.j % 3 != 2 else 2)

		for number in range(1, 10):
			if number in self.notes:
				text = str(number)
				noteLabel = self.noteFont.render(text, 1)
				# TODO

		if self.num:
			text = str(self.num)
			numLabel = self.numberFont.render(text, 1, RED if self.isWrong else BLACK)
			win.blit(numLabel, (self.x+CELL_SIZE//4+5, self.y+CELL_SIZE//4-2))