import pygame, Rectangle

class Car(Rectangle.Rectangle):
	def __init__(self, x, y, w, h):
		super().__init__(x, y, w, h)