import pygame
import os

os.system('cls')
pygame.init()

# Setup display
width, height = 600, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tic Tac Toe')

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PLAYERS = ['X', 'O']
FPS = 60

# Variables
board = [
        ['', '', ''],
        ['', '', ''],
        ['', '', '']
]
currentPlayer = 0
available = []
gameOver = False
w, h = width // 3, height // 3


def drawGrid(win):
    win.fill(WHITE)

    pygame.draw.line(win, BLACK, (w, 0), (w, height), 4)
    pygame.draw.line(win, BLACK, (w * 2, 0), (w * 2, height), 4)
    pygame.draw.line(win, BLACK, (0, h), (width, h), 4)
    pygame.draw.line(win, BLACK, (0, h * 2), (width, h * 2), 4)


def equals(a, b, c):
    return a == b == c and a != ''


def setup():
    for j in range(3):
        for i in range(3):
            available.append([i, j])


def checkWinner():
    winner = None

    # Check vertical
    for i in range(3):
        if equals(board[0][i], board[1][i], board[2][i]):
            winner = [board[0][i], 1, i]

    # Check horizontal
    for i in range(3):
        if equals(board[i][0], board[i][1], board[i][2]):
            winner = [board[i][0], 0, i]

    # Check diagonal
    if equals(board[0][0], board[1][1], board[2][2]):
        winner = [board[0][0], 2]
    if equals(board[0][2], board[1][1], board[2][0]):
        winner = [board[2][0], 3]

    # Check tie
    if winner is None and len(available) == 0:
        winner = 'TIE'

    return winner


def play():
    if not gameOver:
        global currentPlayer
        mouseX, mouseY = pygame.mouse.get_pos()
        col, row = int(mouseX // w), int(mouseY // h)
        if [row, col] in available:
            available.remove([row, col])
            board[row][col] = PLAYERS[currentPlayer]
            currentPlayer = (currentPlayer + 1) % len(PLAYERS)


# Draw line on winning move
def drawWinningMove():
    global gameOver
    result = checkWinner()

    if result is not None and result != 'TIE':
        # Win on horizontal
        if result[1] == 0:
            pygame.draw.line(
                win, RED, (w // 2, result[2] * h + h // 2), (width - w // 2, result[2] * h + h // 2), 20)

        # Win on vertical
        elif result[1] == 1:
            pygame.draw.line(
                win, RED, (result[2] * w + w // 2, h // 2), (result[2] * w + w // 2, height - h // 2), 20)

        # Win on main diagonal (\)
        elif result[1] == 2:
            pygame.draw.line(win, RED, (w // 2, h // 2),
                             (width - w // 2, height - h // 2), 30)

        # Win on secondary diagonal (/)
        elif result[1] == 3:
            pygame.draw.line(win, RED, (width - w // 2, h // 2),
                             (w // 2, height - h // 2), 30)

        gameOver = True

    elif result == 'TIE':
        gameOver = True
        tie_font = pygame.font.SysFont(None, 500)
        tie_label = tie_font.render('TIE', 1, BLACK)
        win.blit(tie_label, (width // 2 - tie_label.get_width() //
                             2, height // 2 - tie_label.get_height() // 2))


def main():
    clock = pygame.time.Clock()
    run = True

    setup()

    while run:
        clock.tick(FPS)

        drawGrid(win)

        if gameOver:
            run = False

        for j in range(3):
            for i in range(3):
                x = w * i + w // 2
                y = h * j + h // 2
                spot = board[j][i]

                if spot == 'X':
                    xr = w // 4
                    pygame.draw.line(
                        win, BLACK, (x - xr, y - xr), (x + xr, y + xr), 8)
                    pygame.draw.line(
                        win, BLACK, (x + xr, y - xr), (x - xr, y + xr), 8)

                elif spot == 'O':
                    pygame.draw.circle(win, BLACK, (x, y), w // 4, 6)

        drawWinningMove()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not gameOver or len(available) > 0:
                    play()

        pygame.display.update()


def mainMenu():
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        win.fill(BLACK)
        start_font = pygame.font.SysFont(None, 50)
        start_label = start_font.render(
            'Press any button to start...', 1, WHITE)
        win.blit(start_label, (width // 2 - start_label.get_width() //
                               2, height // 2 - start_label.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                main()
                run = False

        pygame.display.update()


mainMenu()

pygame.time.delay(2000)
pygame.quit()
