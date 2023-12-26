import itertools
import pygame
import sys


class Chessboard:
    def __init__(self) -> None:
        # Initialize Pygame
        pygame.init()

        # Set up the display
        self.width, self.height = 400, 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Chessboard")

        # Define colors
        self.black = (102, 51, 0)
        self.white = (255, 243, 219)

        # Set the size of each square
        self.square_size = 50

        self.piece_mapping = {
            'p': 'pawnb.png',
            'r': 'rookb.png',
            'n': 'knightb.png',
            'b': 'bishopb.png',
            'q': 'queenb.png',
            'k': 'kingb.png',
            'P': 'pawnw.png',
            'R': 'rookw.png',
            'N': 'knightw.png',
            'B': 'bishopw.png',
            'Q': 'queenw.png',
            'K': 'kingw.png'
        }

    def paint(self, board: dict) -> None:

        a = ''.join(map(lambda x: x.value.icon, board.values()))
        # pieces = [a[i:i + 8] for i in range(0, 64, 8)]
        # pieces = [a[i] for i in range(8)]

        pieces = [''] * 8

        for i in range(8):
            pieces[i % 8] += a[i::8]

        pieces = list(reversed(pieces))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the chessboard
        for row, col in itertools.product(range(8), range(8)):
            color = self.white if (row + col) % 2 == 0 else self.black
            pygame.draw.rect(self.screen, color, (col * self.square_size,
                             row * self.square_size, self.square_size, self.square_size))

            # Draw the pieces
            if pieces[row][col] != '.':
                piece_image = pygame.image.load(
                    self.piece_mapping[pieces[row][col]])
                piece_image = pygame.transform.scale(
                    piece_image, (self.square_size//2, self.square_size//2))
                self.screen.blit(piece_image, (col * self.square_size +
                                 self.square_size//4, row * self.square_size + self.square_size//4))

        pygame.display.flip()
