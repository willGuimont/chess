pieces = ['King', 'Queen', 'Rook', 'Bishop', 'Knight', 'Pawn']

for p in pieces:
    with open(f'{p.lower()}.py', 'w') as f:
        f.write(f'''from board.board import Board
from pieces.piece import Piece


class {p}(Piece):
    def __init__(self, color: Piece.Color):
        super().__init__(color)

    def get_possible_captures(self, board: Board) -> [Piece]:
        pass

    def get_possible_moves(self, board: 'Board') -> set:
        pass

''')
