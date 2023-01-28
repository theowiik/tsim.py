from enum import Enum
from typing import List


class CellType(Enum):
    EMPTY = 0
    TRACK = 1


class Cell:
    def __init__(self, cell_type: CellType, has_train: bool = False):
        self.cell_type = cell_type
        self.has_train = has_train


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
            [Cell(CellType.EMPTY), Cell(CellType.TRACK, True), Cell(CellType.TRACK), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(
                CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY)],
            [Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.TRACK), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(
                CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY)],
            [Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(
                CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY)],
            [Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(
                CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY), Cell(CellType.EMPTY)],
        ]


class Train:
    cargo_length: float = 100.0

    def __init__(self, x: float, y: float, movement_speed: float):
        self.x = x
        self.y = y
        self.movement_speed = movement_speed

    def move(self):
        self.x += self.movement_speed


class World:
    trains: List[Train] = []
    matrix: List[List[Cell]] = DevUtils.create_sample_matrix()

    train_index = (1, 1)

    def __init__(self):
        self.trains.append(Train(200, 200, 1.0))
        self.trains.append(Train(300, 300, 7.0))

    def update(self):
        # Dynamic trains
        for train in self.trains:
            train.move()

        # Static trains
        self.update_matrix()

    def update_matrix(self):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue

                # Ignore diagonal
                if i != 0 and j != 0:
                    continue

                if self.matrix[self.train_index[0] + i][self.train_index[1] + j].cell_type == CellType.TRACK:
                    next_index = (self.train_index[0] + i, self.train_index[1] + j)

                    self.matrix[next_index[0]][next_index[1]].has_train = True
                    self.matrix[self.train_index[0]][self.train_index[1]].has_train = False
                    self.train_index = next_index

                    print("Train moved to: ", self.train_index)
                    return
