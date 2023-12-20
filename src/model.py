from typing import List, Tuple
from core.data import ArrayUtils, Cell, CellType, Direction, DirectionUtils, Train
from core.map_parser import MapParser


class World:
    _direction_utils = DirectionUtils()
    _matrix: List[List[Cell]] = MapParser.build_map()
    _TRAIN_OK_STATE = "OK"
    _TRAIN_CRASH_STATE = "CRASHED"
    is_accelerating = False

    train_positions: dict[Train, any] = {
        Train(Direction.RIGHT): [(1, 2)],
        Train(Direction.UP): [(7, 10)],
    }

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

    def _get_cells_train(self, x, y):
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

        dirs_to_try = [train.direction]

        for direction in self._direction_utils.allowed_turns[train.direction]:
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

            if self._matrix[new_test_y][new_test_x].cell_type == CellType.TRACK:
                (next_x, next_y) = (new_test_x, new_test_y)

        if next_x is not None and next_y is not None:
            (old_x, old_y) = head
            ArrayUtils.push_first(self.train_positions[train], (next_x, next_y))

            new_dir = self._direction_utils.coordinate_to_dir[
                (next_x - old_x, next_y - old_y)
            ]
            train.direction = new_dir
        else:
            # print("💥 no move possible, collision")
            train._state = self._TRAIN_CRASH_STATE

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
                train_on_cell = self._get_cells_train(position[0], position[1])

                if train_on_cell == None:
                    continue

                if train_on_cell != train:
                    # print("💥 collision with another train")
                    train._state = self._TRAIN_CRASH_STATE
                    train_on_cell._state = self._TRAIN_CRASH_STATE
