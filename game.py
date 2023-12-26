
class Piece:
    def __init__(self, color: str) -> None:
        self.color = color
        self.move_multiplier = 1


class Pawn(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.movement = ['nn', 'n', 'nw', 'ne']


class Knight(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.movement = ['nnw', 'nne', 'nee',
                         'nww', 'see', 'sww', 'ssw', 'sse']


class Rook(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.movement = ['n', 's', 'e', 'w']
        self.move_multiplier = 7


class Bishop(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.movement = ['nw', 'sw', 'ne', 'se']
        self.move_multiplier = 7


class Queen(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.movement = ['n', 's', 'e', 'w', 'nw', 'sw', 'ne', 'se']
        self.move_multiplier = 7


class King(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.movement = ['n', 's', 'e', 'w', 'nw', 'sw', 'ne', 'se']


class Empty(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)


class Tile:
    def __init__(self, **kwargs) -> None:
        self.color = kwargs['color'] if 'color' in kwargs else ''
        self.n = kwargs['n'] if 'n' in kwargs else None
        self.s = kwargs['s'] if 's' in kwargs else None
        self.w = kwargs['w'] if 'w' in kwargs else None
        self.e = kwargs['e'] if 'e' in kwargs else None
        self.nw = kwargs['nw'] if 'nw' in kwargs else None
        self.ne = kwargs['ne'] if 'ne' in kwargs else None
        self.sw = kwargs['sw'] if 'sw' in kwargs else None
        self.se = kwargs['se'] if 'se' in kwargs else None

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

        for letter in letters:
            for number in numbers:
                tile_name = letter + number
                self.chessboard[tile_name] = Tile()

        for letter in letters:
            for number in numbers:
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
        repr_str = '   a b c d e f g h\n'
        repr_str += ' +----------------\n'
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
                            piece = Pawn('w' if char.isupper() else 'b')
                        case 'n' | 'N':
                            piece = Knight('w' if char.isupper() else 'b')
                        case 'r' | 'R':
                            piece = Rook('w' if char.isupper() else 'b')
                        case 'b' | 'B':
                            piece = Bishop('w' if char.isupper() else 'b')
                        case 'q' | 'Q':
                            piece = Queen('w' if char.isupper() else 'b')
                        case 'k' | 'K':
                            piece = King('w' if char.isupper() else 'b')

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
