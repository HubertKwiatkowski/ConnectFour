from functools import reduce
import numpy as np
import pygame
import sys

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


ROW_COUND = 6
COLUMN_COUNT = 7
SIZE = 100
RADIUS = SIZE/2-5
width = COLUMN_COUNT * SIZE
height = (ROW_COUND + 1) * SIZE

size = (width, height)


def create_board():
    board = np.zeros((ROW_COUND, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUND-1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUND):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUND):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUND-2):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUND - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUND):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUND):
            pygame.draw.rect(
                screen, BLUE, (c*SIZE, height - (r+1) * SIZE, SIZE, SIZE))
            COLOR = BLACK
            if board[r][c] == 1: COLOR = RED
            if board[r][c] == 2: COLOR = GREEN

            pygame.draw.circle(
                screen, COLOR, ((c*SIZE + SIZE/2), height - (r+1)*SIZE + SIZE/2), RADIUS)

    pygame.display.update()


board = create_board()
game_over = False
turn = 0

pygame.init()
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myFont = pygame.font.SysFont("monospace", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            posx = event.pos[0]
            color = None
            if turn == 0: color = RED
            else: color = GREEN
            pygame.draw.rect(screen, BLACK, ((0, 0), (width, SIZE)))
            pygame.draw.circle(screen, color, (posx, SIZE/2), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            # Ask for Player 1 Input
            if turn == 0:
                posx = event.pos[0]
                col = posx // SIZE
                print(col)

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        pygame.draw.rect(screen, BLACK, ((0, 0), (width, SIZE)))
                        label = myFont.render("Player 1 wins.", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over=True

            # Ask for Player 2 Input
            else:
                posx=event.pos[0]
                col=posx // SIZE
                print(col)

                if is_valid_location(board, col):
                    row=get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        pygame.draw.rect(screen, BLACK, ((0, 0), (width, SIZE)))
                        label = myFont.render("Player 2 wins.", 1, GREEN)
                        screen.blit(label, (40, 10))
                        game_over=True

            draw_board(board)

            turn += 1
            turn=turn % 2

            if game_over:
                pygame.time.wait(3000)
