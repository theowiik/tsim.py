from core.data import Cell, CellType


class MapParser:
    @staticmethod
    def build_map() -> list[list[Cell]]:
        """
        Builds a map by reading the contents of the 'data/map.map' file.

        Returns:
            A 2D list of Cell objects representing the map.
        """
        f = open("data/map.map", "r")
        matrix: list[list[CellType]] = []

        for line in f:
            row: list[Cell] = []

            for char in line.strip().replace("\n", ""):
                cell_type: CellType = MapParser.parse_cell_type(char)
                if cell_type is None:
                    raise ValueError("Cell cannot be None")
                row.append(Cell(cell_type))

            matrix.append(row)

        return matrix

    @staticmethod
    def parse_cell_type(char: str) -> CellType:
        """
        Parses a character to a CellType
        """
        for cell_type in CellType:
            if cell_type.value == char:
                return cell_type

        raise ValueError(f"Invalid character {char} for CellType")
