import copy
from typing import Callable

from board.chess.board import Board
from pieces import piece_utils
from pieces.piece import Piece


class King(Piece):
    def __init__(self, color: Piece.Color):
        super().__init__(color)
        self.__directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    def get_possible_captures(self, board: Board, turn: int) -> set:
        captures = piece_utils.line_of_sight_captures(board, self, self.__directions, 1)
        captures = set(filter(lambda x: self.__can_move_there(board, x, turn), captures))
        return set(captures)

    def __can_move_there(self, board: Board, captured: Piece, turn: int):
        b = copy.deepcopy(board)
        b.set_is_simulation(True)
        s = copy.deepcopy(self)
        position = captured.get_position()
        b.capture(s, b.get_piece_at(position).get(), turn)
        return not b.is_tile_attacked(s.get_color(), position, turn)

    def get_possible_moves(self, board: 'Board', turn: int) -> set:
        position = self.get_position()
        moves = piece_utils.line_of_sight_moves(board, position, self.__directions, 1)

        board.set_is_simulation(True)
        board.remove_piece_at(position)
        color = self.get_color()
        moves = set(filter(lambda x: not board.is_tile_attacked(color, x, turn), moves))
        board.set_piece_at(position, self)
        board.set_is_simulation(False)

        return set(moves)

    def can_capture_cause_check(self, board: Board, piece: Piece, c: Piece, turn: int):
        return self.__can_save_if(board, piece, turn, lambda b, s: b.capture(s, c, turn))

    def can_move_cause_check(self, board: Board, piece: Piece, m: (int, int), turn: int):
        return self.__can_save_if(board, piece, turn, lambda b, s: b.move(s, m, turn))

    def __can_save_if(self, board: Board, piece: Piece, turn: int, action: Callable[[Board, Piece], None]):
        b = copy.deepcopy(board)
        b.set_is_simulation(True)
        s = copy.deepcopy(piece)
        action(b, s)
        return b.is_tile_attacked(s.get_color(), self.get_position(), turn)

    def is_check(self, board: Board, turn: int):
        return board.is_tile_attacked(self.get_color(), self.get_position(), turn)

    def can_move(self, board: Board, turn: int):
        return len(self.get_possible_moves(board, turn)) > 0
