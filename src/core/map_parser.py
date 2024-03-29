from typing import List, Tuple

from core.data import Cell, CellType, SwitchState
from core.util import none_or_whitespace


class MapParser:
    _COMMENT = "//"
    _MAPPINGS: List[Tuple[CellType, List[str]]] = [
        (CellType.EMPTY, ["░", " "]),
        (CellType.TRACK, ["═", "║", "╔", "╚", "╗", "╝", "╬"]),
        (CellType.SWITCH_LEFT, ["╣"]),
        (CellType.SWITCH_RIGHT, ["╠"]),
    ]

    @staticmethod
    def build_map() -> list[list[Cell]]:
        """
        Builds a map by reading the contents of the 'data/map.map' file.

        Returns:
            A 2D list of Cell objects representing the map.
        """
        f = open("data/map.map", "r", encoding="utf-8")
        matrix: list[list[CellType]] = []

        for line in f:
            if none_or_whitespace(line):
                continue

            if line.strip().startswith(MapParser._COMMENT):
                continue

            row: list[Cell] = []

            for char in line.strip().replace("\n", ""):
                cell: Cell = MapParser.parse_cell(char)

                if cell is None:
                    raise ValueError("Cell cannot be None")

                row.append(cell)

                if cell in [CellType.SWITCH_LEFT, CellType.SWITCH_RIGHT]:
                    cell.switch_state = SwitchState.UP

            matrix.append(row)

        if len(matrix) == 0:
            raise ValueError("Empty map! Please configure the map.")

        return matrix

    @staticmethod
    def parse_cell(char: str) -> Cell:
        """
        Parses a character to a Cell.

        Assumes that no whitespace characters are passed.
        """

        match = next(
            (cell_type for cell_type, chars in MapParser._MAPPINGS if char in chars),
            None,
        )

        if match is not None:
            return Cell(match)

        # for (cell_type, chars) in MapParser._MAPPINGS:
        #     for c in chars:
        #         if c == char:
        #             return cell_type

        try:
            sensor_id = int(char)
            return Cell(CellType.SENSOR, sensor_id)
        except Exception:
            pass

        raise ValueError(f"Invalid character {char} for CellType")
