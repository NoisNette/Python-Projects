import numpy as np
import pygame
import math
import os

os.system('cls')
pygame.init()

rows = 6
cols = 7

blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

click = pygame.mixer.Sound('click.wav')


def createBoard():
	board = np.zeros((6, 7))
	return board


def dropPiece(board, row, col, piece):
	board[row][col] = piece
	click.play()


def isValidLocation(board, col):  # If the top row is free, the column is available
	return board[rows - 1][col] == 0


def getNextOpenRow(board, col):
	for r in range(rows):
		if board[r][col] == 0:
			return r


def printBoard(board):
	print(np.flip(board, 0))


def winningMove(board, piece):
	# Check horizontals
	for c in range(cols - 3):
		for r in range(rows):
			if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
				return True

	# Check verticals
	for c in range(cols):
		for r in range(rows - 3):
			if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
				return True

	# Check positive diagonals (/)
	for c in range(cols - 3):
		for r in range(rows - 3):
			if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
				return True

	# Check negative diagonals (\)
	for c in range(cols - 3):
		for r in range(3, rows):
			if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
				return True


def drawBoard(board):
	for c in range(cols):
		for r in range(rows):
			pygame.draw.rect(
				win, blue, (c * sqLen, r * sqLen + sqLen, sqLen, sqLen))
			pygame.draw.circle(
				win, black, (int(c * sqLen + sqLen / 2), int(r * sqLen + 1.5 * sqLen)), radius)

	for c in range(cols):
		for r in range(rows):
			if board[r][c] == 1:
				pygame.draw.circle(
					win, red, (int(c * sqLen + sqLen / 2), height - int(r * sqLen + sqLen / 2)), radius)
			elif board[r][c] == 2:
				pygame.draw.circle(win, yellow, (int(
					c * sqLen + sqLen / 2), height - int(r * sqLen + sqLen / 2)), radius)
	pygame.display.update()


# Initalizations
board = createBoard()
# print(".")
# printBoard(board)
gameOver = False
turn = 0

pygame.init()

sqLen = 100
width = cols * sqLen
height = (rows + 1) * sqLen
radius = int(sqLen / 2 - 5)

size = (width, height)
win = pygame.display.set_mode(size)
drawBoard(board)
pygame.display.update()

font = pygame.font.SysFont('monospace', 75)

pygame.display.set_caption("Connect4")

# MAIN GAME LOOP
while not gameOver:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(win, black, (0, 0, width, sqLen))
			posx = event.pos[0]
			if turn % 2 == 0:
				pygame.draw.circle(win, red, (posx, int(sqLen / 2)), radius)
			else:
				pygame.draw.circle(win, yellow, (posx, int(sqLen / 2)), radius)
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(win, black, (0, 0, width, sqLen))
			# Player 1 Input
			if turn % 2 == 0:
				posx = event.pos[0]
				col = int(posx // sqLen)

				if isValidLocation(board, col):
					row = getNextOpenRow(board, col)
					dropPiece(board, row, col, 1)

					if winningMove(board, 1):
						label = font.render("Player 1 Wins!", 1, red)
						win.blit(label, (40, 10))
						gameOver = True

			# Player 2 Input
			else:
				posx = event.pos[0]
				col = int(posx // sqLen)

				if isValidLocation(board, col):
					row = getNextOpenRow(board, col)
					dropPiece(board, row, col, 2)

					if winningMove(board, 2):
						label = font.render("Player 2 Wins!", 1, yellow)
						win.blit(label, (40, 10))
						gameOver = True

			drawBoard(board)
			turn += 1
			# printBoard(board)
			if gameOver:
				pygame.time.wait(3000)
