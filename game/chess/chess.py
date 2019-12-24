import copy

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
    PIECES = [lambda x: None, Knight, Bishop, Queen, lambda x: None, Bishop, Knight, lambda x: None]
    BOARD_SIZE = 8

    def __init__(self):
        self.__board = Board(self.BOARD_SIZE, self.BOARD_SIZE)
        self.__player_turn = Piece.Color.WHITE
        self.__turn = 1
        self.__initial_configuration()

    def __initial_configuration(self):
        for i, p in enumerate(self.PIECES):
            x = p(Piece.Color.WHITE)
            if x is not None:
                self.__board.set_piece_at((i, 0), x)
        for i in range(self.BOARD_SIZE):
            self.__board.set_piece_at((i, 1), Pawn(Piece.Color.WHITE))

        self.__white_king = King(Piece.Color.WHITE)
        left_white_rook = Rook(Piece.Color.WHITE, self.__white_king)
        right_white_rook = Rook(Piece.Color.WHITE, self.__white_king)
        self.__board.set_piece_at((4, 0), self.__white_king)
        self.__board.set_piece_at((0, 0), left_white_rook)
        self.__board.set_piece_at((7, 0), right_white_rook)

        for i, p in enumerate(self.PIECES):
            x = p(Piece.Color.BLACK)
            if x is not None:
                self.__board.set_piece_at((i, 7), x)
        for i in range(self.BOARD_SIZE):
            self.__board.set_piece_at((i, 6), Pawn(Piece.Color.BLACK))

        self.__black_king = King(Piece.Color.BLACK)
        left_black_rook = Rook(Piece.Color.BLACK, self.__black_king)
        right_black_rook = Rook(Piece.Color.BLACK, self.__black_king)
        self.__board.set_piece_at((4, 7), self.__black_king)
        self.__board.set_piece_at((0, 7), left_black_rook)
        self.__board.set_piece_at((7, 7), right_black_rook)

    def __next_turn(self):
        self.__player_turn = Piece.Color.BLACK if self.__player_turn == Piece.Color.WHITE else Piece.Color.WHITE
        self.__turn += 1

    def get_possible_captures_for(self, piece: Piece) -> set:
        color = piece.get_color()
        king = self.__white_king if color == Piece.Color.WHITE else self.__black_king

        captures = piece.get_possible_captures(self.__board, self.__turn)

        if self.__is_check(self.__board, king):
            captures = list(filter(lambda c: self.__can_capture_save_king(piece, king, c), captures))

        captures = set(filter(lambda c: not self.__can_capture_cause_check(king, piece, c), captures))

        return set(map(lambda x: x.get_position(), captures))

    def __can_capture_cause_check(self, king, piece, c):
        b = copy.deepcopy(self.__board)
        s = copy.deepcopy(piece)
        position = c.get_position()
        b.capture(s, b.get_piece_at(position).get(), self.__turn)
        return b.is_tile_attacked(s.get_color(), king.get_position(), self.__turn)

    def get_possible_moves_for(self, piece: Piece) -> set:
        color = piece.get_color()
        king = self.__white_king if color == Piece.Color.WHITE else self.__black_king
        moves = piece.get_possible_moves(self.__board, self.__turn)

        if self.__is_check(self.__board, king) and piece != king:
            moves = set(filter(lambda m: self.__can_move_save_king(piece, king, m), moves))

        moves = set(filter(lambda m: not self.__can_move_cause_check(king, piece, m), moves))

        return moves

    def __can_move_cause_check(self, king, piece, m):
        b = copy.deepcopy(self.__board)
        s = copy.deepcopy(piece)
        b.move(s, m, self.__turn)
        return b.is_tile_attacked(s.get_color(), king.get_position(), self.__turn)

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
        if captured not in piece.get_possible_captures(self.__board,
                                                       self.__turn) or captured.get_color() == piece.get_color():
            raise InvalidMove('Cannot capture that')
        self.__board.capture(piece, captured, self.__turn)
        self.__next_turn()

    def move(self, piece: Piece, to_pos: (int, int)):
        if piece.get_color() != self.__player_turn:
            raise BadPlayerException('Bad player')
        if to_pos not in piece.get_possible_moves(self.__board, self.__turn):
            raise InvalidMove('Cannot move there')
        self.__board.move(piece, to_pos, self.__turn)
        self.__next_turn()

    def get_player_color(self) -> Piece.Color:
        return self.__player_turn

    def __is_check(self, board, king):
        return board.is_tile_attacked(king.get_color(), king.get_position(), self.__turn)

    def __is_check_mate(self, king):
        can_save_king = self.__can_save_king(king)
        can_king_move = len(king.get_possible_moves(self.__board, self.__turn)) > 0
        is_king_checked = self.__is_check(self.__board, king)
        return is_king_checked and not can_king_move and not can_save_king

    def __can_save_king(self, king):
        pieces = self.__board.get_pieces()
        color = king.get_color()
        pieces = filter(lambda x: x.get_color() == color, pieces)
        for p in pieces:
            if p == king:
                continue
            for m in p.get_possible_moves(self.__board, self.__turn):
                if self.__can_move_save_king(p, king, m):
                    return True
            for c in p.get_possible_captures(self.__board, self.__turn):
                if self.__can_capture_save_king(p, king, c):
                    return True
        return False

    def __can_move_save_king(self, piece, king, m):
        if piece == king:
            return False
        board = copy.deepcopy(self.__board)
        p = copy.deepcopy(piece)
        board.move(p, m, self.__turn)
        if not self.__is_check(board, king):
            return True
        return False

    def __can_capture_save_king(self, piece, king, c):
        if piece == king:
            return False
        board = copy.deepcopy(self.__board)
        p = copy.deepcopy(piece)
        board.capture(p, c, self.__turn)
        if not self.__is_check(board, king):
            return True
        return False

    def get_winner(self):
        if self.__is_check_mate(self.__white_king):
            return Piece.Color.BLACK
        elif self.__is_check_mate(self.__black_king):
            return Piece.Color.WHITE
        return None
