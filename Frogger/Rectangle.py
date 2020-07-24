import pygame

class Rectangle:
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

	def intersects(self, other):
		return self.rect.colliderect(other.rect)