from core.data import Cell, CellType, SwitchState


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
                cell: Cell = MapParser.parse_cell(char)

                if cell is None:
                    raise ValueError("Cell cannot be None")

                row.append(cell)

                if cell in [CellType.SWITCH_LEFT, CellType.SWITCH_RIGHT]:
                    cell.switch_state = SwitchState.UP

            matrix.append(row)

        return matrix

    @staticmethod
    def parse_cell(char: str) -> Cell:
        """
        Parses a character to a Cell.

        Assumes that no whitespace characters are passed.
        """
        for cell_type in CellType:
            if cell_type.value == char:
                return Cell(cell_type)

        try:
            sensor_id = int(char)
            return Cell(CellType.SENSOR, sensor_id)
        except Exception:
            pass

        raise ValueError(f"Invalid character {char} for CellType")
