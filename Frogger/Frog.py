import pygame, Rectangle

class Frog(Rectangle.Rectangle):
	def __init__(self, x, y, w):
		super().__init__(x, y, w, w)

	def draw(self, win):
		pygame.draw.rect(win, (255, 255, 255), self.rect)