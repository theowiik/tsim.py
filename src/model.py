from enum import Enum
from typing import List
import pprint


class CellType(Enum):
    EMPTY = 0
    TRACK = 1


class Cell:
    def __init__(self, cell_type: CellType):
        self.cell_type = cell_type


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

    @staticmethod
    def build_map():
        # TODO: no error handling
        f = open("src/data/map.map", "r")

        matrix = []

        for line in f:
            row = []

            for char in line:
                if char == ".":
                    row.append(Cell(CellType.EMPTY))
                elif char == "#":
                    row.append(Cell(CellType.TRACK))

            matrix.append(row)

        return matrix


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Train:
    cargo_length: float = 100.0
    state = "OK"

    def __init__(self, movement_speed: float, direction: Direction):
        self.movement_speed = movement_speed
        self.direction = direction

    def move(self):
        self.x += self.movement_speed


class World:
    matrix: List[List[Cell]] = DevUtils.build_map()
    train_ok_state = "OK"
    train_crash_state = "CRASHED"

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

    train_positions = {
        Train(1.0, Direction.RIGHT): (2, 1),
        Train(1.0, Direction.LEFT): (1, 1),
    }

    def update(self):
        self.tick()

    def cell_has_train(x, y):
        for _, position in self.train_positions.items():
            if position[0] == x and position[1] == y:
                return True

        return False

    def tick(self):
        for train, position in self.train_positions.items():
            dirs_to_try = [train.direction]

            for direction in self.allowed_turns[train.direction]:
                dirs_to_try.append(direction)

            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(dirs_to_try)
            pp.pprint(train.direction)

            (next_x, next_y) = (None, None)
            for direction in dirs_to_try:
                add_x, add_y = self.dir_to_coordinate[direction]
                new_test_x = position[0] + add_x
                new_test_y = position[1] + add_y

                # Check if new position is valid
                if new_test_x < 0 or new_test_x >= len(self.matrix[0]):
                    continue
                if new_test_y < 0 or new_test_y >= len(self.matrix):
                    continue

                if self.matrix[new_test_y][new_test_x].cell_type == CellType.TRACK:
                    (next_x, next_y) = (new_test_x, new_test_y)

            if next_x is not None and next_y is not None:
                (old_x, old_y) = position
                self.train_positions[train] = (next_x, next_y)
                new_dir = self.coordinate_to_dir[(next_x - old_x, next_y - old_y)]
                train.direction = new_dir

            else:
                print("no move possible 💣")
                train.state = self.train_crash_state
