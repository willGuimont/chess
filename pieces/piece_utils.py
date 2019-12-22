import functools
import itertools

from board.chess.board import Board
from pieces.piece import Piece
from utils.maybe import Maybe


def __line_indexes(board: Board, from_position: (int, int), step: (int, int), max_step: int) -> [(int, int)]:
    w, h = board.get_size()
    dx, dy = step
    x, y = from_position
    x, y = x + dx, y + dy
    out = []
    num_steps = 1
    while 0 <= x < w and 0 <= y < h and num_steps <= max_step:
        out.append((x, y))
        x, y = x + dx, y + dy
        num_steps += 1
    return out


def __line_of_sight(board: Board, from_position: (int, int), step: (int, int), max_step: int) -> [(int, int)]:
    indexes = __line_indexes(board, from_position, step, max_step)
    return list(itertools.takewhile(lambda x: board.get_piece_at(x).is_nothing(), indexes))


def __get_first_seen_in_direction(board: Board, from_position: (int, int), step: (int, int),
                                  max_step: int = float('inf')) -> Maybe:
    indexes = __line_indexes(board, from_position, step, max_step)
    pieces = map(lambda x: board.get_piece_at(x), indexes)
    pieces = list(itertools.dropwhile(lambda x: x.is_nothing(), pieces))
    if len(pieces) == 0:
        return Maybe.nothing()
    else:
        return Maybe.just(pieces[0].get())


def line_of_sight_captures(board: Board, piece: Piece, directions: [(int, int)], max_step: int = float('inf')) \
        -> set:
    position = piece.get_position()
    captures = functools.reduce(lambda x, y: x + [__get_first_seen_in_direction(board, position, y, max_step)],
                                directions, [])
    captures = filter(lambda x: x.is_just(), captures)
    captures = list(map(lambda x: x.get(), captures))
    return set(filter(lambda x: x.get_color() != piece.get_color(), captures))


def line_of_sight_moves(board: Board, position: (int, int), directions: [(int, int)], max_step: int = float('inf')) \
        -> set:
    return set(functools.reduce(lambda x, y: x + __line_of_sight(board, position, y, max_step), directions, []))
