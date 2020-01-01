import traceback

import pyglet

from game.chess.chess import Chess
from interfaces.chess.gui.ui_board import UIBoard
from pieces.piece import Piece
from utils.maybe import Maybe


class Game(pyglet.window.Window):
    WHITE_PIECE_COLOR = (255, 255, 255, 255)
    BLACK_PIECE_COLOR = (0, 0, 0, 255)
    WHITE_TILE_COLOR = (0, 1, 0, 1)
    BLACK_TILE_COLOR = (1, 0, 0, 1)

    TILE_SIZE = 52
    PIECE_SIZE = 40

    def __init__(self):
        super().__init__(width=640, height=600, caption='Chess')
        self.__chess = Chess()
        self.__ui = UIBoard((self.__chess.BOARD_SIZE, self.__chess.BOARD_SIZE), self.WHITE_PIECE_COLOR,
                            self.BLACK_PIECE_COLOR, self.WHITE_TILE_COLOR,
                            self.BLACK_TILE_COLOR, self.TILE_SIZE, self.PIECE_SIZE, self.width, self.height)

        self.__selected_piece = Maybe.nothing()
        self.__winner = None

    def on_draw(self):
        self.clear()
        self.__ui.draw_board(self.__chess)
        if self.__selected_piece.is_just():
            try:
                p = self.__selected_piece.get()
                possible_captures = self.__chess.get_possible_captures_for(p)
                possible_moves = self.__chess.get_possible_moves_for(p)
                self.__ui.draw_captures(p, possible_captures)
                self.__ui.draw_moves(p, possible_moves)
                self.__ui.draw_selected_piece(p)
            except Exception as e:
                print(e)
                print(traceback.print_exc())
        if self.__winner is not None:
            winner = 'White' if self.__winner == Piece.Color.WHITE else 'Black'
            label = pyglet.text.Label(f'Winner: {winner}',
                                      font_size=32,
                                      color=(255, 255, 255, 255),
                                      x=self.width / 2, y=50,
                                      anchor_x='center', anchor_y='center')
            label.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.__winner is not None:
            return
        i, j = self.__ui.get_cell_index_from_mouse_position(x, y)
        if 0 <= i < self.__chess.BOARD_SIZE and 0 <= j < self.__chess.BOARD_SIZE:
            if self.__selected_piece.is_nothing():
                maybe_piece = self.__chess.get_maybe_piece_at((i, j))
                if maybe_piece.is_just():
                    p = maybe_piece.get()
                    if p.get_color() == self.__chess.get_player_color():
                        self.__selected_piece = maybe_piece
            else:
                pos = (i, j)
                if pos == self.__selected_piece.get().get_position():
                    self.__selected_piece = Maybe.nothing()
                else:
                    p = self.__selected_piece.get()
                    possible_captures = self.__chess.get_possible_captures_for(p)
                    possible_moves = self.__chess.get_possible_moves_for(p)
                    if pos in possible_captures:
                        self.__chess.capture(p, pos)
                        self.__selected_piece = Maybe.nothing()
                    elif pos in possible_moves:
                        self.__chess.move(p, pos)
                        self.__selected_piece = Maybe.nothing()
        self.__winner = self.__chess.get_winner()


def run():
    window = Game()
    pyglet.app.run()
