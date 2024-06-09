import pygame
import os
import random

os.system("cls")
pygame.init()
pygame.font.init()

# Setup game display
width, height = 800, 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Minesweeper")

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIGHT_GREY = (192, 192, 192)
MID_GREY = (150, 150, 150)
DARK_GREY = (127, 127, 127)
NUMBER_COLORS = [
    (0, 0, 255),  # Blue 1
    (0, 127, 0),  # Green 2
    RED,  # Red 3
    (50, 0, 100),  # Purple 4
    (127, 0, 0),  # Brown 5
    (0, 127, 127),  # Cyan 6
    BLACK,  # Black 7
    (127, 127, 127),  # Grey 8
]

FPS = 60

SPAWN_MINES_BY_CHANCE = False
MINE_NUMBER = 60
MINE_PERC = 0.15

w = 40  # Width of single spot in pixels
rows = height // w
cols = width // w

# Load images and sounds
mine = pygame.transform.scale(pygame.image.load("mine.png"), (w - 5, w - 5))
boom = pygame.mixer.Sound("boom.wav")
font = pygame.font.Font("visitor1.ttf", w)

# Variables
grid = []
game_over_type = 0


class Spot:
    def __init__(self, i, j, w, mine):
        """
        Constructor for Spot object

        Args:
                i (int): Spot's row index
                j (int): Spot's column index
                w (int): Width of Spot
        """
        self.i = i
        self.j = j
        self.x = j * w
        self.y = i * w
        self.w = w

        self.rect = pygame.Rect(self.x, self.y, self.w, self.w)

        self.mine = mine
        self.revealed = False
        self.flagged = False

        self.neighbors = 0

    def draw(self, win):
        """
        Draw Spot on display

        Args:
                win (Surface): Main display surface
        """
        if self.flagged:  # Draw flag if Spot is flagged
            label = font.render("X", 1, RED)
            win.blit(
                label,
                (
                    self.x + self.w // 2 - label.get_width() // 2 + 1,
                    self.y + self.w // 2 - label.get_height() // 2,
                ),
            )

        if self.revealed:
            if self.mine:  # Draw mine if present
                win.blit(mine, (self.x + 1, self.y + 1))

            else:  # Draw a blank square and number of neighbors if any
                pygame.draw.rect(
                    win, LIGHT_GREY, (self.x + 1, self.y + 1, self.w - 1, self.w - 1)
                )

                if self.neighbors > 0:
                    label = font.render(
                        str(self.neighbors), 1, NUMBER_COLORS[self.neighbors - 1]
                    )
                    win.blit(
                        label,
                        (
                            self.x + self.w // 2 - label.get_width() // 2 + 1,
                            self.y + self.w // 2 - label.get_height() // 2,
                        ),
                    )

        else:
            pygame.draw.line(
                win, WHITE, (self.x + 2, self.y), (self.x + 2, self.y + self.w), width=3
            )  # Left white
            pygame.draw.line(
                win, WHITE, (self.x, self.y + 2), (self.x + self.w, self.y + 2), width=3
            )  # Top white
            pygame.draw.line(
                win,
                MID_GREY,
                (self.x + self.w - 2, self.y),
                (self.x + self.w - 2, self.y + self.w),
                width=3,
            )  # Right grey
            pygame.draw.line(
                win,
                MID_GREY,
                (self.x, self.y + self.w - 2),
                (self.x + self.w, self.y + self.w - 2),
                width=3,
            )  # Bottom grey

        pygame.draw.rect(win, DARK_GREY, self.rect, 1)  # Draw outline of square

    def countNeighbors(self):
        """
        Count number of Spots around this Spot that have a mine, return if this spot has a mine
        """
        if self.mine:
            self.neighbors = -1
            return

        total = 0
        for xoff in range(-1, 2):
            for yoff in range(-1, 2):
                i = self.i + xoff
                j = self.j + yoff
                if (i > -1 and i < cols) and (j > -1 and j < rows):
                    total += grid[i][j].mine

        self.neighbors = total

    def reveal(self):
        """
        Reveal self if clicked
        """
        if self.flagged:
            return

        if self.revealed:
            flagged = 0
            for xoff in range(-1, 2):
                for yoff in range(-1, 2):
                    i = self.i + xoff
                    j = self.j + yoff
                    if (i > -1 and i < cols) and (j > -1 and j < rows):
                        # if grid[i][j].flagged:
                        # print(i, j, end=' | ')
                        flagged += grid[i][j].flagged

            # print(flagged, end='\n\n')
            if flagged != self.neighbors:
                return

            # When a spot which has as many neighbors revealed as its number of neighbors, it can be clicked to automatically reveal all the remaining unrevealed neighbors
            for xoff in range(-1, 2):
                for yoff in range(-1, 2):
                    i = self.i + xoff
                    j = self.j + yoff
                    if (
                        (i > -1 and i < cols)
                        and (j > -1 and j < rows)
                        and not grid[i][j].revealed
                    ):
                        grid[i][j].reveal()

        self.revealed = True

        if self.mine:  # If mine is clicked, game over
            global game_over_type
            game_over_type = -1

        if self.neighbors == 0:
            self.floodFill()

    def floodFill(self):
        """
        Reveal all neighbors which don't have mines
        """
        for xoff in range(-1, 2):
            for yoff in range(-1, 2):
                i = self.i + xoff
                j = self.j + yoff
                if (i > -1 and i < cols) and (j > -1 and j < rows):
                    neighbor = grid[i][j]
                    if not neighbor.mine and not neighbor.revealed:
                        neighbor.reveal()


def setup():
    global grid

    # Create mine layout seed
    if SPAWN_MINES_BY_CHANCE:
        mines = int(rows * cols * MINE_PERC)
        seed = [True] * mines + [False] * (rows * cols - mines)
    else:
        seed = [True] * MINE_NUMBER + [False] * (rows * cols - MINE_NUMBER)

    random.shuffle(seed)

    # Initialize grid
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(Spot(i, j, w, seed[i * cols + j]))
        grid.append(row)

    for row in grid:
        for spot in row:
            spot.countNeighbors()


def draw(win):
    """
    Draw everything to the screen

    Args:
            win (Surface): Main display surface
    """
    win.fill(LIGHT_GREY)

    for row in grid:
        for spot in row:
            spot.draw(win)

    pygame.display.update()


def main():
    """
    Main game function with loop
    """
    global game_over_type
    run = True
    clock = pygame.time.Clock()

    setup()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    x, y = pygame.mouse.get_pos()
                    i, j = y // w, x // w
                    if not grid[i][j].flagged:
                        grid[i][j].reveal()

                if event.button == 3:  # Right click
                    x, y = pygame.mouse.get_pos()
                    i, j = y // w, x // w
                    grid[i][j].flagged = not grid[i][j].flagged

        draw(win)

        # Check if every mine-free spot has been revealed
        got_all = True
        for row in grid:
            for spot in row:
                if not spot.mine and not spot.revealed:
                    got_all = False
        if got_all:
            game_over_type = 1

        if game_over_type:
            run = False

    # Reveal all spots
    for row in grid:
        for spot in row:
            spot.revealed = True
    draw(win)

    # Victory
    if game_over_type == 1:
        font = pygame.font.Font(None, 100)
        label = font.render("YOU WIN!", 1, BLACK)
        win.blit(
            label,
            (
                width // 2 - label.get_width() // 2,
                height // 2 - label.get_height() // 2,
            ),
        )

    # Loss
    if game_over_type == -1:
        boom.play()
        font = pygame.font.Font(None, 100)
        label = font.render("YOU LOSE!", 1, BLACK)
        win.blit(
            label,
            (
                width // 2 - label.get_width() // 2,
                height // 2 - label.get_height() // 2,
            ),
        )

    pygame.display.update()

    # Start a new loop to detect when the user closes the window
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


if __name__ == "__main__":
    main()
