from board.chess.board import Board
from pieces import piece_utils
from pieces.piece import Piece


class Bishop(Piece):
    def __init__(self, color: Piece.Color):
        super().__init__(color)
        self.__directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    def get_possible_captures(self, board: Board, turn: int) -> set:
        return piece_utils.line_of_sight_captures(board, self, self.__directions)

    def get_possible_moves(self, board: 'Board', turn: int) -> set:
        return piece_utils.line_of_sight_moves(board, self.get_position(), self.__directions)
