from enum import Enum
from typing import List


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
    def create_sample_matrix():
        return [
            [Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(
                CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY)],
            [Cell(CellType.EMPTY), Cell(CellType.TRACK), Cell(CellType.TRACK), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(
                CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY)],
            [Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.TRACK), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(
                CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY)],
            [Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(
                CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY)],
            [Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(
                CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY)],
        ]

    @staticmethod
    def build_map():
        # TODO: no error handling
        f = open("data/map.map", "r")

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

    def __init__(self, movement_speed: float, direction: Direction):
        self.movement_speed = movement_speed
        self.direction = direction

    def move(self):
        self.x += self.movement_speed


class World:
    matrix: List[List[Cell]] = DevUtils.build_map()

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
        Train(1.0, Direction.RIGHT): (1, 1),
    }

    def __init__(self):
        pass

    def get_train_positions(self):
        return self.train_positions.values()

    def update(self):
        self.tick()

    def tick(self):
        for train, position in self.train_positions.items():
            dirs = []
            dirs.append(train.direction)
            for direction in self.allowed_turns[train.direction]:
                dirs.append(direction)

            i = 0
            for direction in dirs:
                i += 1
                add_x, add_y = self.dir_to_coordinate[direction]

                new_x = position[0] + add_x
                new_y = position[1] + add_y

                # check if new position is valid
                if new_x < 0 or new_x >= len(self.matrix[0]):
                    continue
                if new_y < 0 or new_y >= len(self.matrix):
                    continue

                # check if new position is track
                if self.matrix[new_y][new_x].cell_type != CellType.TRACK:
                    # count directions

                    if i == len(dirs):
                        print('booom 💣')

                    continue

                # move train
                self.train_positions[train] = (new_x, new_y)

                new_dir = self.coordinate_to_dir[(add_x, add_y)]
                train.direction = new_dir
