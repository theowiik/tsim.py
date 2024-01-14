from enum import Enum
from typing import List, Tuple
from core.data import Cell, CellType, Direction, DirectionUtils
from core.map_parser import MapParser
from core.util import ArrayUtils


class TrainStates(Enum):
    OK = "OK"
    CRASHED = "CRASHED"


class Train:
    state: TrainStates = TrainStates.OK
    is_accelerating: bool = False
    _speed: float = 0
    _deacceleration: float = 0.1
    _acceleration: float = 0.2
    _max_speed: float = 400
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


class Model:
    _direction_utils = DirectionUtils()
    _matrix: List[List[Cell]] = MapParser.build_map()
    is_accelerating = False
    train_positions: dict[Train, list[Tuple]] = {Train(Direction.LEFT): [(24, 1)]}

    def __init__(self):
        for train, positions in self.train_positions.items():
            for _ in range(train._length - 1):
                positions.append((positions[0][0], positions[0][1]))

    def tick(self):
        """
        Main tick function
        """
        for train, positions in self.train_positions.items():
            self._move_train_tick(train, positions)

        self._check_collisions()

    def get_cells_train(self, x, y) -> Train | None:
        for train, positions in self.train_positions.items():
            for position in positions:
                if position[0] == x and position[1] == y:
                    return train

        return None

    def _move_train_tick(self, train: Train, positions: List[Tuple[int, int]]):
        for _ in range(train.get_rounded_speed()):
            self._move_train_one_cell(train, positions)

        # TOOD: bad
        train.is_accelerating = self.is_accelerating
        train.accelerate_tick()

    def _move_train_one_cell(
        self, train: Train, positions: List[Tuple[int, int]]
    ) -> None:
        """
        Moves the train one cell in the direction specified by the train's current direction.
        If a valid move is found, updates the train's position and direction accordingly.
        If no valid move is found, sets the train's state to TRAIN_CRASH_STATE.

        Args:
            train (Train): The train object to move.
            positions (List[Tuple[int, int]]): The current positions of all trains.

        Returns:
            None
        """
        head = positions[0]
        current_cell: Cell = self._matrix[head[1]][head[0]]

        dirs_to_try: list[Direction] = [train.direction]

        for direction in self._direction_utils.allowed_turns[train.direction]:
            # Ensure it's a valid direction
            if direction in current_cell._allowed_turns:
                dirs_to_try.append(direction)

        (next_x, next_y) = (None, None)
        for direction in dirs_to_try:
            add_x, add_y = self._direction_utils.dir_to_coordinate[direction]
            new_test_x = head[0] + add_x
            new_test_y = head[1] + add_y

            if new_test_x < 0 or new_test_x >= len(self._matrix[0]):
                continue
            if new_test_y < 0 or new_test_y >= len(self._matrix):
                continue

            if self._matrix[new_test_y][new_test_x].cell_type in [
                CellType.TRACK,
                CellType.SWITCH_LEFT,
                CellType.SWITCH_RIGHT,
            ]:
                (next_x, next_y) = (new_test_x, new_test_y)
                break

        if next_x is not None and next_y is not None:
            (old_x, old_y) = head
            ArrayUtils.push_first(self.train_positions[train], (next_x, next_y))

            new_dir = self._direction_utils.coordinate_to_dir[
                (next_x - old_x, next_y - old_y)
            ]
            train.direction = new_dir
        else:
            # print("💥 no move possible, collision")
            train.state = TrainStates.CRASHED

    def _check_collisions(self):
        """
        Checks for collisions between trains and updates their states accordingly.

        This method iterates over each train and its positions, and checks if there is
        another train occupying the same position. If a collision is detected, both
        trains are set to the `TRAIN_CRASH_STATE`.

        Note: This method assumes that the train positions have already been updated.

        Returns:
            None
        """
        for train, positions in self.train_positions.items():
            for position in positions:
                train_on_cell = self.get_cells_train(position[0], position[1])

                if train_on_cell is None:
                    continue

                if train_on_cell != train:
                    # print("💥 collision with another train")
                    train.state = self._TRAIN_CRASH_STATE
                    train_on_cell.state = self._TRAIN_CRASH_STATE
