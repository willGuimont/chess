from board.chess.board import Board
from pieces.chess.bishop import Bishop
from pieces.chess.king import King
from pieces.chess.knight import Knight
from pieces.chess.pawn import Pawn
from pieces.chess.queen import Queen
from pieces.chess.rook import Rook
from pieces.piece import Piece
from utils.maybe import Maybe


class BadPlayerException(Exception):
    ...


class InvalidMove(Exception):
    ...


class NoSuchPiece(Exception):
    ...


class Chess:
    PIECES = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    BOARD_SIZE = 8

    def __init__(self):
        self.__board = Board(self.BOARD_SIZE, self.BOARD_SIZE)
        self.__player_turn = Piece.Color.WHITE
        self.__initial_configuration()

    def __initial_configuration(self):
        for i, p in enumerate(self.PIECES):
            self.__board.set_piece_at((i, 0), p(Piece.Color.WHITE))
        for i in range(self.BOARD_SIZE):
            self.__board.set_piece_at((i, 1), Pawn(Piece.Color.WHITE))
        for i, p in enumerate(self.PIECES):
            self.__board.set_piece_at((i, 7), p(Piece.Color.BLACK))
        for i in range(self.BOARD_SIZE):
            self.__board.set_piece_at((i, 6), Pawn(Piece.Color.BLACK))

    def __next_turn(self):
        self.__player_turn = Piece.Color.BLACK if self.__player_turn == Piece.Color.WHITE else Piece.Color.WHITE

    def get_possible_captures_for(self, piece: Piece) -> set:
        return set(map(lambda x: x.get_position(), piece.get_possible_captures(self.__board)))

    def get_possible_moves_for(self, piece: Piece) -> set:
        return piece.get_possible_moves(self.__board)

    def get_maybe_piece_at(self, position: (int, int)) -> Maybe:
        return self.__board.get_piece_at(position)

    def __get_piece_at(self, position: (int, int)) -> Piece:
        piece = self.__board.get_piece_at(position)
        if piece.is_nothing():
            raise NoSuchPiece(f'Not piece at position {position}')
        return piece.get()

    def capture(self, piece: Piece, captured_position: (int, int)):
        if piece.get_color() != self.__player_turn:
            raise BadPlayerException('Bad player')
        captured = self.__get_piece_at(captured_position)
        if captured not in piece.get_possible_captures(self.__board) or captured.get_color() == piece.get_color():
            raise InvalidMove('Cannot capture that')
        self.__board.capture(piece, captured)
        self.__next_turn()

    def move(self, piece: Piece, to_pos: (int, int)):
        if piece.get_color() != self.__player_turn:
            raise BadPlayerException('Bad player')
        if to_pos not in piece.get_possible_moves(self.__board):
            raise InvalidMove('Cannot move there')
        self.__board.move(piece, to_pos)
        self.__next_turn()

    def get_player_color(self) -> Piece.Color:
        return self.__player_turn
