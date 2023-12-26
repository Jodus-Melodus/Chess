
import itertools


class Piece:
    def __init__(self, color: str) -> None:
        self.color = color
        self.move_multiplier = 1

    def __repr__(self) -> str:
        return self.icon if self.color == 'black' else self.icon.upper()


class Pawn(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.icon = 'p'
        self.movement = ['nn', 'n', 'nw', 'ne']


class Knight(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.icon = 'n'
        self.movement = ['nnw', 'nne', 'nee',
                         'nww', 'see', 'sww', 'ssw', 'sse']


class Rook(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.icon = 'r'
        self.movement = ['n', 's', 'e', 'w']
        self.move_multiplier = 7


class Bishop(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.icon = 'b'
        self.movement = ['nw', 'sw', 'ne', 'se']
        self.move_multiplier = 7


class Queen(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.icon = 'q'
        self.movement = ['n', 's', 'e', 'w', 'nw', 'sw', 'ne', 'se']
        self.move_multiplier = 7


class King(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.icon = 'k'
        self.movement = ['n', 's', 'e', 'w', 'nw', 'sw', 'ne', 'se']


class Empty(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.icon = '.'


class Tile:
    def __init__(self, **kwargs) -> None:
        self.color = kwargs.get('color', '')
        self.n = kwargs.get('n', None)
        self.e = kwargs.get('e', None)
        self.s = kwargs.get('s', None)
        self.w = kwargs.get('w', None)
        self.ne = kwargs.get('ne', None)
        self.se = kwargs.get('se', None)
        self.sw = kwargs.get('sw', None)
        self.nw = kwargs.get('nw', None)

        self.value = Empty(self.color)

    def __str__(self) -> str:
        return f'{self.value}'

    def __repr__(self) -> str:
        return f'''
value:{str(self.value)}
color:{str(self.color)}
n:{str(self.n)}
s:{str(self.s)}
w:{str(self.w)}
e:{str(self.e)}
nw:{str(self.nw)}
ne:{str(self.ne)}
sw:{str(self.sw)}
se:{str(self.se)}
'''


class Move:
    def __init__(self, origin: Tile, destination: Tile) -> None:
        self.origin = origin
        self.destination = destination

    def __repr__(self) -> str:
        return f'{self.origin} -> {self.destination}'


class ChessBoard:
    def __init__(self) -> None:
        letters = 'abcdefgh'
        numbers = '12345678'
        self.chessboard = {}

        for letter, number in itertools.product(letters, numbers):
            tile_name = letter + number
            self.chessboard[tile_name] = Tile()

        for letter, number in itertools.product(letters, numbers):
            tile_name = letter + number
            tile = self.chessboard[tile_name]

            tile.n = self.chessboard.get(letter + str(int(number) + 1))
            tile.s = self.chessboard.get(letter + str(int(number) - 1))
            tile.e = self.chessboard.get(chr(ord(letter) + 1) + number)
            tile.w = self.chessboard.get(chr(ord(letter) - 1) + number)
            tile.ne = self.chessboard.get(
                chr(ord(letter) + 1) + str(int(number) + 1))
            tile.se = self.chessboard.get(
                chr(ord(letter) + 1) + str(int(number) - 1))
            tile.nw = self.chessboard.get(
                chr(ord(letter) - 1) + str(int(number) + 1))
            tile.sw = self.chessboard.get(
                chr(ord(letter) - 1) + str(int(number) - 1))

    def __repr__(self) -> str:
        repr_str = '   a b c d e f g h\n' + ' +----------------\n'
        for rank in range(8, 0, -1):
            repr_str += f'{rank}| '
            for file in range(97, 105):
                key = chr(file) + str(rank)
                piece = self.chessboard.get(key)
                repr_str += f'{piece} '
            repr_str += '\n'
        return repr_str + ' +----------------\n   a b c d e f g h'

    def generate_board(self, fen: str = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1') -> None:
        self.fen = fen
        fen = fen.split(' ')

        piece_placement = fen[0]
        self.active_color = fen[1]
        self.castling_availability = fen[2]
        self.en_passant_target = fen[3]
        self.halfmove_clock = int(fen[4])
        self.fullmove_number = int(fen[5]) if len(fen) > 5 else 1

        rows = piece_placement.split('/')

        for rank, row in enumerate(rows):
            file = 1
            for char in row:
                if char.isdigit():
                    file += int(char)
                else:
                    index = chr(96 + file) + str(8 - rank)
                    match char:
                        case 'p' | 'P':
                            piece = Pawn(
                                'white' if char.isupper() else 'black')
                        case 'n' | 'N':
                            piece = Knight(
                                'white' if char.isupper() else 'black')
                        case 'r' | 'R':
                            piece = Rook(
                                'white' if char.isupper() else 'black')
                        case 'b' | 'B':
                            piece = Bishop(
                                'white' if char.isupper() else 'black')
                        case 'q' | 'Q':
                            piece = Queen(
                                'white' if char.isupper() else 'black')
                        case 'k' | 'K':
                            piece = King(
                                'white' if char.isupper() else 'black')

                    self.chessboard[index].value = piece
                    file += 1

    def generate_moves(self) -> list[Move]:
        moves = []

        for filerank, piece in self.chessboard:
            if isinstance(piece, Empty):
                continue


if __name__ == '__main__':
    board = ChessBoard()

    board.generate_board()
    print(board)
