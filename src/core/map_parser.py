from src.model import Cell, CellType


class MapParser:
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
