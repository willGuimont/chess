from pieces.piece import Piece


class PlaceHolder(Piece):

    def __init__(self, color: Piece.Color):
        super().__init__(color)

    def get_possible_captures(self, board: 'Board', turn: int) -> set:
        return set()

    def get_possible_moves(self, board: 'Board', turn: int) -> set:
        return set()
