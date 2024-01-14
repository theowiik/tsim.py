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
            SwitchState.DOWN: [Direction.DOWN, Direction.LEFT],
        },
        CellType.SWITCH_RIGHT: {
            SwitchState.UP: [Direction.UP, Direction.RIGHT],
            SwitchState.DOWN: [Direction.DOWN, Direction.RIGHT],
        },
    }

    _allowed_turns: list[Direction] = []
    _switch_state: SwitchState = SwitchState.NONE

    def __init__(self, cell_type: CellType):
        self.cell_type = cell_type

        if self.cell_type == CellType.TRACK:
            self._allowed_turns = [
                Direction.UP,
                Direction.DOWN,
                Direction.LEFT,
                Direction.RIGHT,
            ]
        else:
            self._allowed_turns = [Direction.UP]

    @property
    def switch_state(self) -> SwitchState:
        return self._switch_state

    @switch_state.setter
    def switch_state(self, switch_state: SwitchState) -> None:
        self._switch_state = switch_state

        if self.cell_type in [CellType.SWITCH_LEFT, CellType.SWITCH_RIGHT]:
            self._allowed_turns = self._directions_map[self.cell_type][switch_state]
        else:
            self._allowed_turns = [
                Direction.UP,
                Direction.DOWN,
                Direction.LEFT,
                Direction.RIGHT,
            ]


class DirectionUtils:
    DIR_TO_COORDINATE: dict[Direction, tuple[int, int]] = {
        Direction.UP: (0, -1),
        Direction.DOWN: (0, 1),
        Direction.LEFT: (-1, 0),
        Direction.RIGHT: (1, 0),
    }

    COORDINATE_TO_DIR: dict[tuple[int, int], Direction] = {
        (0, -1): Direction.UP,
        (0, 1): Direction.DOWN,
        (-1, 0): Direction.LEFT,
        (1, 0): Direction.RIGHT,
    }

    ALLOWED_TURNS: dict[Direction, List[Direction]] = {
        Direction.UP: [Direction.LEFT, Direction.RIGHT],
        Direction.DOWN: [Direction.LEFT, Direction.RIGHT],
        Direction.LEFT: [Direction.UP, Direction.DOWN],
        Direction.RIGHT: [Direction.UP, Direction.DOWN],
    }
