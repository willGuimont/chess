from pieces.piece import Piece
from pieces.placeholder import PlaceHolder
from utils.flatmap import flatmap
from utils.maybe import Maybe


class Board:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__board = [Maybe.nothing()] * (self.__width * self.__height)

    def get_piece_at(self, position: (int, int)) -> Maybe:
        x, y = position
        if not (0 <= x < self.__width) or not (0 <= y < self.__height):
            raise IndexError(f'{position} out of range')
        return self.__board[x + y * self.__width]

    def __set_at(self, position: (int, int), value: Maybe):
        x, y = position
        if not (0 <= x < self.__width) or not (0 <= y < self.__height):
            raise IndexError()
        self.__board[x + y * self.__width] = value

    def set_piece_at(self, position: (int, int), piece: Piece):
        self.__set_at(position, Maybe.just(piece))
        piece.set_pos(position)

    def remove_piece_at(self, position: (int, int)):
        self.__set_at(position, Maybe.nothing())

    def capture_piece(self, piece: Piece):
        position = piece.get_position()
        self.remove_piece_at(position)

    def get_size(self):
        return self.__width, self.__height

    def move(self, piece: Piece, to_position: (int, int), turn: int):
        piece.move(self, to_position, turn)

    def capture(self, piece: Piece, captured: Piece, turn: int):
        piece.capture(self, captured, turn)

    def get_pieces(self):
        pieces = []
        for p in self.__board:
            if p.is_just():
                x = p.get()
                pieces.append(x)
        return pieces

    def is_tile_attacked(self, color: Piece.Color, position: (int, int), turn: int):
        pieces = self.get_pieces()
        attackers = list(filter(lambda p: p.get_color() != color, pieces))

        piece = self.get_piece_at(position)
        is_tile_empty = piece.is_nothing()
        is_attacked = False

        if is_tile_empty:
            piece = PlaceHolder(color)
            self.set_piece_at(position, piece)
        else:
            piece = piece.get()

        attacked = list(flatmap(lambda x: x.get_possible_captures(self, turn), attackers))
        if piece in attacked:
            is_attacked = True

        if is_tile_empty:
            self.remove_piece_at(piece.get_position())

        return is_attacked
