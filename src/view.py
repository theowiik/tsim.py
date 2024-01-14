import threading
import time
import pygame
from pygame import Surface
from core.data import Cell, CellType, Direction
from model import Train, TrainStates, Model
from rich.console import Console
from rich.table import Table
from rich.live import Live


class View:
    _CELL_WIDTH: int = 20
    _CELL_MARGIN: int = 2
    _CELL_NONE_COLOR: tuple[int, int, int] = (136, 75, 75)
    _CELL_TRACK_COLOR: tuple[int, int, int] = (136, 136, 75)
    _CELL_TRAIN_COLORS: list[tuple[int, int, int]] = [(75, 75, 136), (66, 123, 123)]
    _CELL_TRAIN_CRASH_COLOR: tuple[int, int, int] = (200, 20, 20)
    _CLEAR_COLOR: tuple[int, int, int] = (43, 42, 41)

    def __init__(self, model: Model, screen: Surface):
        self._model = model
        self._screen = screen
        terminal_thread = threading.Thread(target=self._print_terminal)
        terminal_thread.start()

    def draw(self) -> None:
        """
        Main draw function
        """
        self._screen.fill(self._CLEAR_COLOR)
        self._draw_matrix()
        pygame.display.update()

    def _print_terminal(self) -> None:
        """
        Display info in terminal live
        """
        with Live(self._generate_info_table(), refresh_per_second=4) as live:
            while True:
                time.sleep(0.2)
                live.update(self._generate_info_table())

    def _render_text(self, text: str, x: int, y: int) -> None:
        font = pygame.font.Font(None, 20)
        text = font.render(text, True, (0, 0, 0))
        self._screen.blit(text, (x, y))

    def _get_direction_symbol(self, direction: Direction) -> str:
        if direction == Direction.UP:
            return "^"
        elif direction == Direction.DOWN:
            return "v"
        elif direction == Direction.LEFT:
            return "<"
        elif direction == Direction.RIGHT:
            return ">"

        return "?"

    def _draw_matrix(self) -> None:
        yoffset = self._CELL_MARGIN
        y_index = 0

        for row in self._model._matrix:
            xoffset = self._CELL_MARGIN
            x_index = 0

            for cell in row:
                color = self._CELL_NONE_COLOR
                train: Train | None = self._model.get_cells_train(x_index, y_index)

                if train is not None:
                    if train.state == TrainStates.CRASHED:
                        color = self._CELL_TRAIN_CRASH_COLOR
                    else:
                        color = self._CELL_TRAIN_COLORS[0]

                elif cell.cell_type in [
                    CellType.TRACK,
                    CellType.SWITCH_LEFT,
                    CellType.SWITCH_RIGHT,
                ]:
                    color = self._CELL_TRACK_COLOR

                pygame.draw.rect(
                    self._screen,
                    color,
                    pygame.Rect(
                        xoffset,
                        yoffset,
                        self._CELL_WIDTH,
                        self._CELL_WIDTH,
                    ),
                )

                # Draw allowed turns
                if cell.cell_type in [
                    CellType.SWITCH_LEFT,
                    CellType.SWITCH_RIGHT,
                ]:
                    mask = self._build_direction_mask(cell)
                    self._render_text(mask, xoffset, yoffset)

                x_index += 1
                xoffset += self._CELL_WIDTH + self._CELL_MARGIN

            y_index += 1
            yoffset += self._CELL_WIDTH + self._CELL_MARGIN

    def _build_direction_mask(self, cell: Cell) -> str:
        return "".join(
            [
                "^" if Direction.UP in cell._allowed_turns else "",
                "v" if Direction.DOWN in cell._allowed_turns else "",
                "<" if Direction.LEFT in cell._allowed_turns else "",
                ">" if Direction.RIGHT in cell._allowed_turns else "",
            ]
        )

    def _generate_info_table(self) -> Table:
        # print("generate_info_table")
        table = Table(title="Info")
        table.add_column("Train", justify="center", style="cyan")
        table.add_column("Speed", justify="center", style="magenta")

        i = 0
        for train, _ in self._model.train_positions.items():
            table.add_row(str(i), str(train.get_rounded_speed()))
            i += 1

        return table
