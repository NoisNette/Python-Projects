import pygame
from random import choice
from functools import partial

from config import *

from cell import Cell
from button import Button, ToggleButton, NumButton
from gameGenerator import GameGenerator

pygame.init()
pygame.font.init()

class App:
	def __init__(self):
		self.win = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption('Sudoku')

		self.grid = [[Cell(i, j, 175, 100, 0, 0, True) for j in range(9)] for i in range(9)]
		self.newGame()

		self.usePencil = False

		self.commands = [
			Button('Nova igra', 200, 565, 50, 50, self.newGame),
			Button('Reset', 315, 565, 50, 50, self.reset),
			Button('Briši', 435, 565, 50, 50, self.erase),
			ToggleButton('Olovka', 555, 565, 50, 50, self.pencil),
		]
		self.buttons = [
			NumButton('1', 47, 660, 74, 74, partial(self.clickNumButton, 1)),
			NumButton('2', 126, 660, 74, 74, partial(self.clickNumButton, 2)),
			NumButton('3', 205, 660, 74, 74, partial(self.clickNumButton, 3)),
			NumButton('4', 284, 660, 74, 74, partial(self.clickNumButton, 4)),
			NumButton('5', 363, 660, 74, 74, partial(self.clickNumButton, 5)),
			NumButton('6', 442, 660, 74, 74, partial(self.clickNumButton, 6)),
			NumButton('7', 521, 660, 74, 74, partial(self.clickNumButton, 7)),
			NumButton('8', 600, 660, 74, 74, partial(self.clickNumButton, 8)),
			NumButton('9', 679, 660, 74, 74, partial(self.clickNumButton, 9)),
		]

		self.selectedSpot = [0, 0, 0]
		self.selectedNumber = self.grid[0][0].num if self.grid[0][0].num else -1

	def chooseRandomCellWithNum(self, num):
		possible = set()
		for i in range(9):
			for j in range(9):
				if self.grid[i][j].num == num:
					possible.add((i, j))

		return choice(list(possible)) if possible else None

	def clickNumButton(self, num):
		i, j, _ = self.selectedSpot
		self.selectedNumber = num if num else -1

		if self.grid[i][j].isEditable:
			self.grid[i][j].mark(num)
		else:
			res = self.chooseRandomCellWithNum(num)
			if res:
				i, j = res
				self.selectedSpot = [i, j, (i // 3) * 3 + (j // 3)]

		if self.foundAll(num):
			self.buttons[num-1].disable()


	def foundAll(self, num):
		return sum(self.grid[i][j].num == num for j in range(9) for i in range(9)) == 9


	def newGame(self):
		grid = GameGenerator.generateGrid()
		
		for i in range(9):
			for j in range(9):
				cellNum, isOriginal = grid[i][j]
				self.grid[i][j].set(
					cellNum if isOriginal else 0,
					cellNum,
					not isOriginal
				)

		for num in range(1, 10):
			if self.foundAll(num):
				self.buttons[num-1].disable()

	def reset(self):
		for i in range(9):
			for j in range(9):
				if self.grid[i][j].isEditable:
					self.grid[i][j].num = 0
		

	def erase(self):
		selectedI, selectedJ, _ = self.selectedSpot
		self.grid[selectedI][selectedJ].erase()
	
	def pencil(self):
		self.usePencil = not self.usePencil

	def draw(self):
		self.win.fill(WHITE)

		for i in range(9):
			for j in range(9):
				cell = self.grid[i][j]
				cell.draw(self.win, self.selectedNumber, *self.selectedSpot)

		for button in self.commands:
			button.draw(self.win)

		for button in self.buttons:
			button.draw(self.win)

		pygame.display.update()

	def run(self):
		shouldRun = True
		clock = pygame.time.Clock()

		while shouldRun:
			clock.tick(FPS)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP and self.selectedSpot[0] > 0:
						self.selectedSpot[0] -= 1
					if event.key == pygame.K_DOWN and self.selectedSpot[0] < 8:
						self.selectedSpot[0] += 1
					if event.key == pygame.K_RIGHT and self.selectedSpot[1] < 8:
						self.selectedSpot[1] += 1
					if event.key == pygame.K_LEFT and self.selectedSpot[1] > 0:
						self.selectedSpot[1] -= 1

					self.selectedSpot[2] = (self.selectedSpot[0] // 3) * 3 + (self.selectedSpot[1] // 3)
				

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1: # Left click
						x, y = pygame.mouse.get_pos()
						for row in self.grid:
							for cell in row:
								if cell.collides(x, y):
									self.selectedSpot = [cell.i, cell.j, cell.quadrant]
									self.selectedNumber = cell.num if cell.num else -1

						for button in self.commands:
							if button.isHovered:
								button.click()

						for button in self.buttons:
							if button.isHovered:
								button.click()

			

			self.draw()

if __name__ == '__main__':
	app = App()
	app.run()