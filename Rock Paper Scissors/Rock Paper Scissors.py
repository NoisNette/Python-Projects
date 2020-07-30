import pygame
import os
import random

os.system('cls')
pygame.init()
pygame.font.init()

# Setup game display
width, height = 600, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Rock Paper Scissors')
pygame.display.set_icon(pygame.image.load(os.path.join('assets', 'icon.png')))

# Load images
dims = (100, 100)
rock = pygame.transform.scale(pygame.image.load(
	os.path.join('assets', 'rock.png')), dims)
paper = pygame.transform.scale(pygame.image.load(
	os.path.join('assets', 'paper.png')), dims)
scissors = pygame.transform.scale(pygame.image.load(
	os.path.join('assets', 'scissors.png')), dims)

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
clock = pygame.time.Clock()
fontPath = os.path.join('assets', 'Montserrat.ttf')

# Variables
playerScore = 0
computerScore = 0


class Button:
	pass


def draw(win):
	win.fill(WHITE)

	# Display title
	font = pygame.font.Font(fontPath, 40)
	label = font.render('Rock Paper Scissors', 1, BLACK)
	win.blit(label, (width // 2 - label.get_width() // 2, 75))

	# Display score
	font = pygame.font.Font(fontPath, 24)
	text = 'Player {} : {} Computer'.format(playerScore, computerScore)
	label = font.render(text, 1, BLACK)
	win.blit(label, (width // 2 - label.get_width() // 2, 175))

	# Display choices

	pygame.display.update()


def main():
	run = True
	while run:
		clock.tick(FPS)

		draw(win)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()


main()
