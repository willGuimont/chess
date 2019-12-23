from abc import ABC, abstractmethod
from enum import Enum


class Piece(ABC):
    class Color(Enum):
        BLACK = 0
        WHITE = 1

    def __init__(self, color: Color):
        self.__color = color
        self.__x = -1
        self.__y = -1
        self.__has_moved = False
        self.__last_moved = 0

    def set_pos(self, position: (int, int)):
        self.__x, self.__y = position

    def get_position(self) -> (int, int):
        return self.__x, self.__y

    def set_has_moved(self, has_moved):
        self.__has_moved = has_moved

    def has_moved(self):
        return self.__has_moved

    def get_color(self):
        return self.__color

    def get_last_moved(self):
        return self.__last_moved

    @abstractmethod
    def get_possible_captures(self, board: 'Board', turn: int) -> set:
        ...

    @abstractmethod
    def get_possible_moves(self, board: 'Board', turn: int) -> set:
        ...

    def move(self, board: 'Board', to_position: (int, int), turn: int):
        position = self.get_position()
        board.set_piece_at(to_position, self)
        board.remove_piece_at(position)
        self.set_has_moved(True)
        self.__last_moved = turn

    def capture(self, board: 'Board', captured, turn: int):
        from_position = self.get_position()
        to_position = captured.get_position()
        board.capture_piece(captured)
        board.remove_piece_at(from_position)
        board.set_piece_at(to_position, self)
        self.set_has_moved(True)
        self.__last_moved = turn
