import pyglet
import pyglet.gl as gl

from game.chess.chess import Chess
from pieces.chess.bishop import Bishop
from pieces.chess.king import King
from pieces.chess.knight import Knight
from pieces.chess.pawn import Pawn
from pieces.chess.queen import Queen
from pieces.chess.rook import Rook
from pieces.piece import Piece


class UIBoard:
    def __init__(self, board_size: (int, int), white_piece_color: (int, int, int, int),
                 black_piece_color: (int, int, int, int), white_tile_color: (int, int, int, int),
                 black_tile_color: (int, int, int, int), tile_size: int, piece_size: int,
                 window_width: int, window_height: int):
        self.__board_size = board_size
        self.__white_piece_color = white_piece_color
        self.__black_piece_color = black_piece_color
        self.__white_tile_color = white_tile_color
        self.__black_tile_color = black_tile_color
        self.__tile_size = tile_size
        self.__half_tile_size = tile_size / 2
        self.__piece_size = piece_size
        self.__window_width = window_width
        self.__window_height = window_height

        self.__board_size_width, self.__board_size_height = self.__board_size
        self.__transform = self.__window_width / 2 - self.__board_size_width / 2 * self.__tile_size, \
                           self.__window_height / 2 - self.__board_size_height / 2 * self.__tile_size, \
                           0

    def get_cell_index_from_mouse_position(self, x: int, y: int):
        x, y = x - self.__transform[0], y - self.__transform[1]
        return int(x // self.__tile_size), int(y // self.__tile_size)

    def draw_board(self, chess: Chess):
        gl.glPushMatrix()
        gl.glTranslatef(*self.__transform)

        for x in range(self.__board_size_width):
            for y in range(self.__board_size_height):
                gl.glPushMatrix()
                gl.glTranslatef(x * self.__tile_size, y * self.__tile_size, 0)
                self.__draw_tile(x, y)
                self.__draw_piece(chess, x, y)
                gl.glPopMatrix()
        gl.glPopMatrix()

    def __draw_tile(self, x: int, y: int):
        tile_color = self.__white_tile_color if (x + y) % 2 == 0 else self.__black_tile_color
        gl.glColor4f(*tile_color)

        gl.glBegin(gl.GL_QUADS)
        gl.glVertex2d(0, 0)
        gl.glVertex2d(self.__tile_size, 0)
        gl.glVertex2d(self.__tile_size, self.__tile_size)
        gl.glVertex2d(0, self.__tile_size)
        gl.glEnd()

    def __draw_piece(self, chess: Chess, x: int, y: int):
        piece = chess.get_maybe_piece_at((x, y))
        if piece.is_nothing():
            return
        piece = piece.get()
        str_piece = self.__show_piece(piece)
        self.__draw_label(piece.get_color(), str_piece, self.__half_tile_size, self.__half_tile_size, self.__piece_size)

    @staticmethod
    def __show_piece(piece: Piece):
        if isinstance(piece, Bishop):
            return '♗'
        elif isinstance(piece, King):
            return '♔'
        elif isinstance(piece, Knight):
            return '♘'
        elif isinstance(piece, Pawn):
            return '♙'
        elif isinstance(piece, Queen):
            return '♕'
        elif isinstance(piece, Rook):
            return '♖'

    def draw_moves(self, piece: Piece, moves: (int, int)):
        color = piece.get_color()
        for m in moves:
            x, y = m
            gl.glPushMatrix()
            gl.glTranslatef(*self.__transform)
            gl.glTranslatef(x * self.__tile_size, y * self.__tile_size, 0)

            self.__draw_label(color, 'M', self.__half_tile_size, self.__half_tile_size, self.__piece_size)

            gl.glPopMatrix()

    def draw_captures(self, piece: Piece, captures: (int, int)):
        color = piece.get_color()
        for c in captures:
            x, y = c
            gl.glPushMatrix()
            gl.glTranslatef(*self.__transform)
            gl.glTranslatef(x * self.__tile_size, y * self.__tile_size, 0)

            self.__draw_label(color, 'C', self.__half_tile_size, self.__half_tile_size, self.__piece_size)

            gl.glPopMatrix()

    def draw_selected_piece(self, selected_piece: Piece):
        x, y = selected_piece.get_position()
        gl.glPushMatrix()
        gl.glTranslatef(*self.__transform)
        gl.glTranslatef(x * self.__tile_size, y * self.__tile_size, 0)

        self.__draw_label(selected_piece.get_color(), '▢', self.__half_tile_size, self.__half_tile_size * 1.4,
                          self.__piece_size * 1.25)

        gl.glPopMatrix()

    def __draw_label(self, color: Piece.Color, char: str, x: float, y: float, font_size: float):
        piece_color = self.__white_piece_color if color == Piece.Color.WHITE else self.__black_piece_color
        label = pyglet.text.Label(char,
                                  font_size=font_size,
                                  color=piece_color,
                                  x=x, y=y,
                                  anchor_x='center', anchor_y='center')
        label.draw()
