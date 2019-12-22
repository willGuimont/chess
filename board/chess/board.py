from pieces.piece import Piece
from utils.maybe import Maybe


class PieceAlreadyPresent(Exception):
    ...


class Board:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__board = [Maybe.nothing()] * (self.__width * self.__height)
        self.__dead_pieces = []

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
        self.get_piece_at(position).if_present(lambda x: self.__dead_pieces.append(x))
        self.remove_piece_at(position)

    def get_size(self):
        return self.__width, self.__height

    def move(self, piece: Piece, to_position: (int, int)):
        starting_pos = piece.get_position()
        if self.get_piece_at(to_position).is_just():
            raise PieceAlreadyPresent(f'could not move from {starting_pos} to {to_position}')
        piece.move(self, to_position)

    def capture(self, piece: Piece, captured: Piece):
        piece.capture(self, captured)
