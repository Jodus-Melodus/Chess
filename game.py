import itertools
import gui
import time
import copy
from alive_progress import alive_bar


class Piece:
    def __init__(self, filerank: str, color: str) -> None:
        self.filerank = filerank
        self.color = color
        self.move_multiplier = 1
        self.movement = ['n', 's', 'e', 'w', 'nw', 'sw', 'ne', 'se']

    def __repr__(self) -> str:
        return self.icon


class Pawn(Piece):
    def __init__(self, filerank: str, color: str) -> None:
        super().__init__(filerank, color)
        self.icon = 'p' if self.color == 'black' else 'P'
        self.movement = ['nn', 'n', 'nw', 'ne'] if self.color == 'white' else [
            'ss', 's', 'sw', 'se']


class Knight(Piece):
    def __init__(self, filerank: str, color: str) -> None:
        super().__init__(filerank, color)
        self.icon = 'n' if self.color == 'black' else 'N'
        self.movement = ['nnw', 'nne', 'nee',
                         'nww', 'see', 'sww', 'ssw', 'sse']


class Rook(Piece):
    def __init__(self, filerank: str, color: str) -> None:
        super().__init__(filerank, color)
        self.icon = 'r' if self.color == 'black' else 'R'
        self.movement = ['n', 's', 'e', 'w']
        self.move_multiplier = 7


class Bishop(Piece):
    def __init__(self, filerank: str, color: str) -> None:
        super().__init__(filerank, color)
        self.icon = 'b' if self.color == 'black' else 'B'
        self.movement = ['nw', 'sw', 'ne', 'se']
        self.move_multiplier = 7


class Queen(Piece):
    def __init__(self, filerank: str, color: str) -> None:
        super().__init__(filerank, color)
        self.icon = 'q' if self.color == 'black' else 'Q'
        self.move_multiplier = 7


class King(Piece):
    def __init__(self, filerank: str, color: str) -> None:
        super().__init__(filerank, color)
        self.icon = 'k' if self.color == 'black' else 'K'


class Empty(Piece):
    def __init__(self, filerank: str, color: str) -> None:
        super().__init__(filerank, color)
        self.icon = '.'


class Tile:
    def __init__(self, filerank: str, **kwargs) -> None:
        self.filerank = filerank
        self.color = kwargs.get('color', '')
        self.n = kwargs.get('n', None)
        self.e = kwargs.get('e', None)
        self.s = kwargs.get('s', None)
        self.w = kwargs.get('w', None)
        self.ne = kwargs.get('ne', None)
        self.se = kwargs.get('se', None)
        self.sw = kwargs.get('sw', None)
        self.nw = kwargs.get('nw', None)

        self.value = Empty(filerank, self.color)

    def __repr__(self) -> str:
        return f'{self.value}'

    def copy(self) -> None:
        return copy.deepcopy(self)


class Move:
    def __init__(self, origin: Tile, destination: Tile) -> None:
        self.origin = origin
        self.destination = destination

    def __repr__(self) -> str:
        return f'{self.origin} -> {self.destination}'


class ChessBoard:
    def __init__(self) -> None:
        self.letters = 'abcdefgh'
        self.numbers = '12345678'
        self.chessboard = {}
        for letter, number in itertools.product(self.letters, self.numbers):
            tile_name = letter + number
            self.chessboard[tile_name] = Tile(tile_name)

    def generate_chessboard(self) -> None:
        for letter, number in itertools.product(self.letters, self.numbers):
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

    def toggle_turn(self) -> None:
        self.active_color = 'black' if self.active_color == 'white' else 'white'

    def generate_board(self, fen: str = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1') -> None:
        self.fen = fen
        fen = fen.split(' ')

        piece_placement = fen[0]
        self.active_color = 'white' if fen[1] == 'w' else 'black'
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
                            piece = Pawn(index,
                                         'white' if char.isupper() else 'black')
                        case 'n' | 'N':
                            piece = Knight(index,
                                           'white' if char.isupper() else 'black')
                        case 'r' | 'R':
                            piece = Rook(index,
                                         'white' if char.isupper() else 'black')
                        case 'b' | 'B':
                            piece = Bishop(index,
                                           'white' if char.isupper() else 'black')
                        case 'q' | 'Q':
                            piece = Queen(index,
                                          'white' if char.isupper() else 'black')
                        case 'k' | 'K':
                            piece = King(index,
                                         'white' if char.isupper() else 'black')

                    self.chessboard[index].value = piece
                    file += 1

    def generate_moves(self) -> list[Move]:
        moves = []

        for filerank, tile in self.chessboard.items():
            if tile.value.color == self.active_color:
                if isinstance(tile.value, Empty):
                    continue

                elif isinstance(tile.value, (Bishop, Rook, Queen, King)):
                    moves.append(self.evaluate_sliding_moves(tile))

                elif isinstance(tile.value, Knight):
                    moves.append(self.evaluate_knight_moves(tile))

                elif isinstance(tile.value, Pawn):
                    moves.append(self.evaluate_pawn_moves(tile))

        print
        return [i for x in moves for i in x]

    def evaluate_sliding_moves(self, tile: Tile) -> list[Move]:
        moves = []
        piece = tile.value

        for direction in piece.movement:
            new_pos = tile
            for _ in range(1, piece.move_multiplier + 1):
                if new_pos:
                    new_pos = getattr(new_pos, direction)
                else:
                    break

                if new_pos:
                    attacked_piece = new_pos.value
                    if isinstance(attacked_piece, Empty):
                        moves.append(Move(tile, new_pos))
                    elif isinstance(attacked_piece, (Pawn, Knight, Bishop, Rook, Queen, King)):
                        if attacked_piece.color != piece.color:
                            moves.append(Move(tile, new_pos))
                        break
        return moves

    def evaluate_knight_moves(self, tile: Tile) -> list[Move]:
        moves = []
        piece = tile.value

        for direction in piece.movement:
            directions = list(direction)
            new_pos = tile
            for direction in directions:
                if new_pos:
                    new_pos = getattr(new_pos, direction)
                else:
                    break

            if new_pos:
                attacked_piece = new_pos.value
                if piece.color != attacked_piece.color:
                    moves.append(Move(tile, new_pos))

        return moves

    def evaluate_pawn_moves(self, tile: Tile) -> list[Move]:
        moves = []
        piece = tile.value

        for direction in piece.movement:

            # Check if pieces can move 2 spaces otherwise skip
            if direction == 'nn' and tile.filerank[1] != '2':
                continue
            if direction == 'ss' and tile.filerank[1] != '7':
                continue

            directions = list(direction)
            new_pos = tile
            for d in directions:
                if new_pos:
                    new_pos = getattr(new_pos, d)
                else:
                    break

            if new_pos:
                attacked_piece = new_pos.value

                if direction in {'nw', 'ne', 'sw', 'se'} and isinstance(new_pos.s.value, Pawn):
                    en_passant_piece = new_pos.s.value
                    if en_passant_piece.color != piece.color and (
                        en_passant_piece.color == 'black'
                        and en_passant_piece.filerank[1] == '5'
                        or en_passant_piece.color != 'black'
                        and en_passant_piece.color == 'white'
                        and en_passant_piece.filerank[1] == '4'
                    ):
                        moves.append(Move(tile, new_pos))

                elif (direction not in ('nw', 'ne', 'sw', 'se') or attacked_piece.color not in (piece.color, '')):
                    if direction in {'nn', 'ss', 'n', 's'} and isinstance(attacked_piece, Empty):
                        moves.append(Move(tile, new_pos))

        return moves

    def make_move(self, move: Move) -> None:
        new_chessboard = dict(self.chessboard)

        # Copy the destination tile and change its value to the origin tile's value
        new_chessboard[move.destination.filerank] = self.chessboard[move.destination.filerank].copy()
        new_chessboard[move.destination.filerank].value = move.origin.value

        # Copy the origin tile and change its value to the destination tile's value
        new_chessboard[move.origin.filerank] = self.chessboard[move.origin.filerank].copy()
        new_chessboard[move.origin.filerank].value = Empty(
            move.origin.filerank, '')

        self.chessboard = new_chessboard

        self.toggle_turn()

    def unmake_move(self, move: Move) -> None:
        new_chessboard = dict(self.chessboard)

        # Copy the origin tile and change its value to the destination tile's value
        new_chessboard[move.origin.filerank] = self.chessboard[move.origin.filerank].copy()
        new_chessboard[move.origin.filerank].value = move.destination.value

        # Copy the destination tile and change its value to the origin tile's value
        new_chessboard[move.destination.filerank] = self.chessboard[move.destination.filerank].copy()
        new_chessboard[move.destination.filerank].value = move.origin.value

        self.chessboard = new_chessboard

        self.toggle_turn()


def calc_total_moves(depth: int, board: ChessBoard, pbar: alive_bar, screen):
    if depth == 0:
        return 1

    moves = board.generate_moves()
    total = 0
    bar()

    for move in moves:
        board.make_move(move)
        screen.paint(board.chessboard)
        total += calc_total_moves(depth - 1, board, pbar, screen)
        board.unmake_move(move)
        screen.paint(board.chessboard)

    return total


if __name__ == '__main__':
    board = ChessBoard()
    screen = gui.Chessboard()
    board.generate_chessboard()
    board.generate_board()

    print(board)

    screen.paint(board.chessboard)

    with alive_bar() as bar:
        ply = 3

        print(calc_total_moves(ply, board, bar, screen))


# 3 -> 7722
# 2 -> 400
# 1 -> 20
