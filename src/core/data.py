from enum import Enum
from typing import List


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class CellType(Enum):
    EMPTY = "."
    TRACK = "#"
    SWITCH_LEFT = "<"
    SWITCH_RIGHT = ">"


class SwitchState(Enum):
    UP = "UP"
    DOWN = "DOWN"
    NONE = "NONE"


class Cell:
    _directions_map = {
        CellType.SWITCH_LEFT: {
            SwitchState.UP: [Direction.UP, Direction.LEFT],
            SwitchState.DOWN: [Direction.DOWN, Direction.RIGHT],
        },
        CellType.SWITCH_RIGHT: {
            SwitchState.UP: [Direction.DOWN, Direction.RIGHT],
            SwitchState.DOWN: [Direction.UP, Direction.LEFT],
        },
    }

    allowed_turns: list[Direction] = []

    switch_state: SwitchState = SwitchState.NONE

    def __init__(self, cell_type: CellType):
        self.cell_type = cell_type

        if self.cell_type == CellType.TRACK:
            self.allowed_turns = [
                Direction.UP,
                Direction.DOWN,
                Direction.LEFT,
                Direction.RIGHT,
            ]
        else:
            self.allowed_turns = [Direction.UP]

    def set_switch_state(self, switch_state: SwitchState) -> None:
        self.switch_state = switch_state

        if self.cell_type in [CellType.SWITCH_LEFT, CellType.SWITCH_RIGHT]:
            self.allowed_turns = self._directions_map[self.cell_type][switch_state]
        else:
            self.allowed_turns = [
                Direction.UP,
                Direction.DOWN,
                Direction.LEFT,
                Direction.RIGHT,
            ]


class DirectionUtils:
    dir_to_coordinate: dict[Direction, tuple[int, int]] = {
        Direction.UP: (0, -1),
        Direction.DOWN: (0, 1),
        Direction.LEFT: (-1, 0),
        Direction.RIGHT: (1, 0),
    }

    coordinate_to_dir: dict[tuple[int, int], Direction] = {
        (0, -1): Direction.UP,
        (0, 1): Direction.DOWN,
        (-1, 0): Direction.LEFT,
        (1, 0): Direction.RIGHT,
    }

    allowed_turns: dict[Direction, List[Direction]] = {
        Direction.UP: [Direction.LEFT, Direction.RIGHT],
        Direction.DOWN: [Direction.LEFT, Direction.RIGHT],
        Direction.LEFT: [Direction.UP, Direction.DOWN],
        Direction.RIGHT: [Direction.UP, Direction.DOWN],
    }


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
