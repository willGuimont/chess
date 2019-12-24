import copy

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
        s = copy.deepcopy(self)
        position = captured.get_position()
        b.capture(s, b.get_piece_at(position).get(), turn)
        return not b.is_tile_attacked(s.get_color(), position, turn)

    def get_possible_moves(self, board: 'Board', turn: int) -> set:
        position = self.get_position()
        moves = piece_utils.line_of_sight_moves(board, position, self.__directions, 1)

        board.remove_piece_at(position)
        color = self.get_color()
        moves = set(filter(lambda x: not board.is_tile_attacked(color, x, turn), moves))

        board.set_piece_at(position, self)
        return set(moves)
