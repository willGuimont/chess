import traceback

import pyglet

from game.chess.chess import Chess
from interfaces.chess.gui.ui_board import UIBoard
from utils.maybe import Maybe


class Game(pyglet.window.Window):
    WHITE_PIECE_COLOR = (255, 255, 255, 255)
    BLACK_PIECE_COLOR = (0, 0, 0, 255)
    WHITE_TILE_COLOR = (0, 255, 0, 255)
    BLACK_TILE_COLOR = (255, 0, 0, 255)

    TILE_SIZE = 52
    PIECE_SIZE = 40

    def __init__(self):
        super().__init__()
        self.chess = Chess()
        self.ui = UIBoard((self.chess.BOARD_SIZE, self.chess.BOARD_SIZE), self.WHITE_PIECE_COLOR,
                          self.BLACK_PIECE_COLOR, self.WHITE_TILE_COLOR,
                          self.BLACK_TILE_COLOR, self.TILE_SIZE, self.PIECE_SIZE, self.width, self.height)

        self.selected_piece = Maybe.nothing()

    def on_draw(self):
        self.clear()
        self.ui.draw_board(self.chess)
        if self.selected_piece.is_just():
            try:
                p = self.selected_piece.get()
                possible_captures = self.chess.get_possible_captures_for(p)
                possible_moves = self.chess.get_possible_moves_for(p)
                self.ui.draw_captures(p, possible_captures)
                self.ui.draw_moves(p, possible_moves)
                self.ui.draw_selected_piece(p)
            except Exception as e:
                print(e)
                print(traceback.print_exc())

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        i, j = self.ui.get_cell_index_from_mouse_position(x, y)
        if 0 <= i < self.chess.BOARD_SIZE and 0 <= j < self.chess.BOARD_SIZE:
            if self.selected_piece.is_nothing():
                maybe_piece = self.chess.get_maybe_piece_at((i, j))
                if maybe_piece.is_just():
                    p = maybe_piece.get()
                    if p.get_color() == self.chess.get_player_color():
                        self.selected_piece = maybe_piece
            else:
                pos = (i, j)
                if pos == self.selected_piece.get().get_position():
                    self.selected_piece = Maybe.nothing()
                else:
                    p = self.selected_piece.get()
                    possible_captures = self.chess.get_possible_captures_for(p)
                    possible_moves = self.chess.get_possible_moves_for(p)
                    if pos in possible_captures:
                        self.chess.capture(p, pos)
                        self.selected_piece = Maybe.nothing()
                    elif pos in possible_moves:
                        self.chess.move(p, pos)
                        self.selected_piece = Maybe.nothing()


def run():
    window = Game()
    pyglet.app.run()
