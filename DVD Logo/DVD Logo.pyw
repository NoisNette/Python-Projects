import pygame
import sys
import os
import random
import time

os.system('cls')
pygame.init()
pygame.font.init()

width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('DVD Logo')

# Load image and sound
dvd = pygame.image.load('dvd_logo.png')
clack = pygame.mixer.Sound('clack.wav')

xs, ys = 3, 3

def move(dvd, x, y):
	global xs
	global ys
	x += xs
	y += ys

	if x <= 0 or x + dvd.get_width() >= width:
		xs *= -1
		clack.play()
	if y <= 0 or y + dvd.get_height() >= height:
		ys *= -1
		clack.play()
	

def main():
	run = True
	FPS = 60
	x, y = 400, 300
	r, g, b = 255, 255, 255

	clock = pygame.time.Clock()

	def redrawWindow():
		win.fill((0, 0, 0))
		dvd.fill((r, g, b), special_flags=pygame.BLEND_ADD)
		win.blit(dvd, (x, y))
	
	def pickColor():
		r = random.randint(100, 255)
		g = random.randint(100, 255)
		b = random.randint(100, 255)

	pickColor()

	while run:
		clock.tick(FPS)
		redrawWindow()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				pickColor()

		move(dvd, x, y)

		pygame.display.update()
	
main()