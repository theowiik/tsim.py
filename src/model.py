from enum import Enum
from typing import List


class CellType(Enum):
    EMPTY = 0
    TRACK = 1


class Cell:
    cell_type: CellType = CellType.EMPTY

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

    def __init__(self):
        self.trains.append(Train(200, 200, 1.0))
        self.trains.append(Train(300, 300, 2.0))

    def update(self):
        for train in self.trains:
            train.move()

        DevUtils.print_matrix(self.matrix)
