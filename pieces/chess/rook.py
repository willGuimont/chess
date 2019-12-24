from board.chess.board import Board
from pieces import piece_utils
from pieces.chess.king import King
from pieces.piece import Piece


class Rook(Piece):
    def __init__(self, color: Piece.Color, king: King):
        super().__init__(color)
        self.__king = king
        self.__directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def get_possible_captures(self, board: Board, turn: int) -> set:
        return piece_utils.line_of_sight_captures(board, self, self.__directions)

    def get_possible_moves(self, board: 'Board', turn: int) -> set:
        moves = piece_utils.line_of_sight_moves(board, self.get_position(), self.__directions)
        moves = moves.union(self.__right_castling(board, turn))
        moves = moves.union(self.__left_castling(board, turn))
        return moves

    def __right_castling(self, board: 'Board', turn: int):
        if not self.has_moved() and not self.__king.has_moved():
            king_position = self.__king.get_position()
            kx, ky = king_position
            color = self.get_color()
            is_king_ok = not board.is_tile_attacked(color, king_position, turn)
            is_self_ok = not board.is_tile_attacked(color, self.get_position(), turn)
            space_1 = (kx + 2, ky)
            is_space_1_ok = board.get_piece_at(space_1).is_nothing() and not board.is_tile_attacked(color, space_1,
                                                                                                    turn)
            space_2 = (kx + 1, ky)
            is_space_2_ok = board.get_piece_at(space_2).is_nothing() and not board.is_tile_attacked(color, space_2,
                                                                                                    turn)
            if is_king_ok and is_self_ok and is_space_1_ok and is_space_2_ok:
                return {(kx, ky)}
        return set()

    def __left_castling(self, board: 'Board', turn: int):
        if not self.has_moved() and not self.__king.has_moved():
            king_position = self.__king.get_position()
            kx, ky = king_position
            color = self.get_color()
            is_king_ok = not board.is_tile_attacked(color, king_position, turn)
            is_self_ok = not board.is_tile_attacked(color, self.get_position(), turn)
            space_1 = (kx - 1, ky)
            is_space_1_ok = board.get_piece_at(space_1).is_nothing() and not board.is_tile_attacked(color, space_1,
                                                                                                    turn)
            space_2 = (kx - 2, ky)
            is_space_2_ok = board.get_piece_at(space_2).is_nothing() and not board.is_tile_attacked(color, space_2,
                                                                                                    turn)
            space_3 = (kx - 3, ky)
            is_space_3_ok = board.get_piece_at(space_2).is_nothing() and not board.is_tile_attacked(color, space_3,
                                                                                                    turn)
            if is_king_ok and is_self_ok and is_space_1_ok and is_space_2_ok and is_space_3_ok:
                return {(kx, ky)}
        return set()

    def move(self, board: 'Board', to_position: (int, int), turn: int):
        castling = to_position == self.__king.get_position()
        if castling:
            left_castling = self.get_position()[0] < to_position[0]

            king_position = self.__king.get_position()
            kx, ky = king_position
            if left_castling:
                to_position = (kx - 1, ky)
                from_position = (kx - 2, ky)
            else:
                to_position = (kx + 2, ky)
                from_position = (kx + 1, ky)
        else:
            from_position = self.get_position()
        super().move(board, to_position, turn)

        if castling:
            board.move(self.__king, from_position, turn)
