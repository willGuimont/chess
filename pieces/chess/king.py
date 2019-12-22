from board.chess.board import Board
from pieces import piece_utils
from pieces.piece import Piece


class King(Piece):
    def __init__(self, color: Piece.Color):
        super().__init__(color)
        self.__directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    def get_possible_captures(self, board: Board) -> set:
        return piece_utils.line_of_sight_captures(board, self, self.__directions, 1)

    def get_possible_moves(self, board: 'Board') -> set:
        # TODO castling
        return piece_utils.line_of_sight_moves(board, self.get_position(), self.__directions, 1)
