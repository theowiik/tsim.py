from enum import Enum
from typing import List
from uuid import uuid4


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class CellType(Enum):
    EMPTY = 1
    TRACK = 2
    SWITCH_LEFT = 3
    SWITCH_RIGHT = 4
    SENSOR = 5


class SwitchState(Enum):
    UP = 1
    DOWN = 2
    NONE = 3


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

    def __init__(self, cell_type: CellType, id: str = None) -> None:
        self.cell_type = cell_type

        if id is None:
            self.id = str(uuid4())

        self.id = id

        if self.cell_type in [CellType.TRACK, CellType.SENSOR]:
            self._allowed_turns = [
                Direction.UP,
                Direction.DOWN,
                Direction.LEFT,
                Direction.RIGHT,
            ]
        elif self.cell_type == CellType.SWITCH_LEFT:
            self._allowed_turns = [Direction.UP, Direction.LEFT]
        elif self.cell_type == CellType.SWITCH_RIGHT:
            self._allowed_turns = [Direction.UP, Direction.RIGHT]
        elif self.cell_type == CellType.EMPTY:
            self._allowed_turns = []
        else:
            raise ValueError(f"Invalid cell type {cell_type}")

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
