from board.chess.board import Board
from pieces import piece_utils
from pieces.chess.bishop import Bishop
from pieces.chess.knight import Knight
from pieces.chess.queen import Queen
from pieces.chess.rook import Rook
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
        p = (x, y + self.__direction)
        moves = set()
        if piece_utils.is_on_board(*p, board) and board.get_piece_at(p).is_nothing():
            moves.add(p)
            if not self.has_moved():
                pp = (x, y + 2 * self.__direction)
                if piece_utils.is_on_board(*pp, board) and board.get_piece_at(pp).is_nothing():
                    moves.add(pp)
        return moves

    def move(self, board: 'Board', to_position: (int, int)):
        super().move(board, to_position)
        self.__check_promotion(board)

    def capture(self, board: 'Board', captured):
        super().capture(board, captured)
        self.__check_promotion(board)

    def __check_promotion(self, board: 'Board'):
        x, y = self.get_position()
        _, h = board.get_size()
        if y == (h - 1 if self.__direction > 0 else 0):
            promotion = ''
            while promotion not in ['q', 'k', 'r', 'b']:
                print('Pawn promotion: (Q)ueen, (K)night, (R)ook, (B)bishop')
                promotion = input('Promote to: ').lower()
            color = self.get_color()
            if promotion == 'q':
                board.set_piece_at((x, y), Queen(color))
            elif promotion == 'k':
                board.set_piece_at((x, y), Knight(color))
            elif promotion == 'r':
                board.set_piece_at((x, y), Rook(color))
            elif promotion == 'b':
                board.set_piece_at((x, y), Bishop(color))
