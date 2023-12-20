from enum import Enum
from typing import List


class CellType(Enum):
    EMPTY = 0
    TRACK = 1


class Cell:
    def __init__(self, cell_type: CellType):
        self.cell_type = cell_type


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class DirectionUtils:
    dir_to_coordinate = {
        Direction.UP: (0, -1),
        Direction.DOWN: (0, 1),
        Direction.LEFT: (-1, 0),
        Direction.RIGHT: (1, 0),
    }

    coordinate_to_dir = {
        (0, -1): Direction.UP,
        (0, 1): Direction.DOWN,
        (-1, 0): Direction.LEFT,
        (1, 0): Direction.RIGHT,
    }

    allowed_turns = {
        Direction.UP: [Direction.LEFT, Direction.RIGHT],
        Direction.DOWN: [Direction.LEFT, Direction.RIGHT],
        Direction.LEFT: [Direction.UP, Direction.DOWN],
        Direction.RIGHT: [Direction.UP, Direction.DOWN],
    }


class Train:
    # TODO: move to model
    state: str = "OK"
    _speed: float = 0
    is_accelerating: bool = False
    _deacceleration: float = 0.1
    _acceleration: float = 0.2
    _max_speed: float = 4
    _length: float = 5

    def __init__(
        self,
        direction: Direction,
    ):
        self.direction: Direction = direction

    def accelerate_tick(self):
        if self.is_accelerating:
            self._speed += self._acceleration
        else:
            self._speed -= self._deacceleration

        # Clamp within [0, _max_speed]
        self._speed = max(min(self._speed, self._max_speed), 0)

    def get_rounded_speed(self):
        return int(self._speed)


class ArrayUtils:
    @staticmethod
    def push_first(a: List[any], v: any) -> None:
        """
        Inserts the value to the first position in
        the array without increasing the size.
        "Pushes" the values down, so the last element
        will dissapear. Destructive method.

        Examples:
        a = [1, 2, 3];
        push_first(a, -4);
        print(a) -> [-4, 1, 2];
        """

        if a is None:
            raise Exception("Array is None")

        if len(a) == 0:
            a.append(v)

        i = len(a) - 1
        while i > 0:
            a[i] = a[i - 1]
            i -= 1

        a[0] = v


class DevUtils:
    @staticmethod
    def print_matrix(matrix: List[List[Cell]]):
        print("---------------------------------")

        for row in matrix:
            for cell in row:
                char = "."

                if cell.cell_type == CellType.TRACK:
                    char = "#"

                print(char, end=" ")
            print()
