from board.chess.board import Board
from pieces import piece_utils
from pieces.piece import Piece


class Pawn(Piece):
    def __init__(self, color: Piece.Color):
        super().__init__(color)
        self.__direction = 1 if color == Piece.Color.WHITE else -1
        self.__captures = [(-1, self.__direction), (1, self.__direction)]

    def get_possible_captures(self, board: Board) -> set:
        # TODO en passant
        return piece_utils.line_of_sight_captures(board, self, self.__captures, 1)

    def get_possible_moves(self, board: 'Board') -> set:
        x, y = self.get_position()
        moves = {(x, y + self.__direction)}
        if not self.has_moved():
            moves.add((x, y + 2 * self.__direction))
        w, h = board.get_size()
        return set(filter(lambda x: 0 <= x[0] <= w and 0 <= x[1] < h, moves))

    def move(self, board: 'Board', to_position: (int, int)):
        # TODO promotion
        super().move(board, to_position)
