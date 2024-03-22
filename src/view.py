import os
import threading
import time

import pygame
from pygame import Surface
from rich.layout import Layout
from rich.live import Live
from rich.table import Table

from core.data import Cell, CellType, Direction
from model import Model, TrainStates


class View:
    _CELL_NONE_COLOR: tuple[int, int, int] = (136, 75, 75)
    _CELL_SENSOR_COLOR: tuple[int, int, int] = (75, 136, 75)
    _CELL_SENSOR_ACTIVE_COLOR: tuple[int, int, int] = (133, 0, 0)
    _CELL_TRACK_COLOR: tuple[int, int, int] = (136, 136, 75)
    _CELL_TRAIN_COLORS: list[tuple[int, int, int]] = [(75, 75, 136), (66, 123, 123)]
    _CELL_TRAIN_CRASH_COLOR: tuple[int, int, int] = (200, 20, 20)
    _CLEAR_COLOR: tuple[int, int, int] = (43, 42, 41)

    def __init__(self, model: Model, screen: Surface):
        self._model = model
        self._screen = screen
        terminal_thread = threading.Thread(target=self._print_terminal)
        terminal_thread.start()
        self._clear_terminal()

    def draw(self) -> None:
        """
        Main draw function
        """
        self._screen.fill(self._CLEAR_COLOR)
        self._draw_matrix()
        pygame.display.update()

    def _clear_terminal(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def _print_terminal(self) -> None:
        """
        Display info in terminal live
        """
        layout = Layout()
        layout.split_row(Layout(name="left"), Layout(name="right"))

        with Live(layout, refresh_per_second=10):
            while True:
                layout["left"].update(self._generate_train_info_table())
                layout["right"].update(self._generate_world_info_table())
                time.sleep(0.1)

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
        cell_size = int(self._calculate_cell_size())

        for y_index, row in enumerate(self._model._matrix):
            for x_index, cell in enumerate(row):
                # Color
                if cell.cell_type == CellType.SENSOR:
                    color = self._CELL_SENSOR_COLOR

                    if self._model.sensor_states[(x_index, y_index)]:
                        color = self._CELL_SENSOR_ACTIVE_COLOR

                elif self._model.get_cells_train(x_index, y_index):
                    train = self._model.get_cells_train(x_index, y_index)
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
                else:
                    color = self._CELL_NONE_COLOR

                # Draw the cell
                pygame.draw.rect(
                    self._screen,
                    color,
                    pygame.Rect(
                        x_index * cell_size,
                        y_index * cell_size,
                        cell_size,
                        cell_size,
                    ),
                )

                # Draw allowed turns for switch cells
                if cell.cell_type in [CellType.SWITCH_LEFT, CellType.SWITCH_RIGHT]:
                    mask = self._build_direction_mask(cell)
                    self._render_text(mask, x_index * cell_size, y_index * cell_size)

    def _build_direction_mask(self, cell: Cell) -> str:
        return "".join(
            [
                "^" if Direction.UP in cell._allowed_turns else "",
                "v" if Direction.DOWN in cell._allowed_turns else "",
                "<" if Direction.LEFT in cell._allowed_turns else "",
                ">" if Direction.RIGHT in cell._allowed_turns else "",
            ]
        )

    def _generate_train_info_table(self) -> Table:
        table = Table(title="Train")
        table.add_column("Train", justify="center", style="cyan")
        table.add_column("Speed", justify="center", style="magenta")
        table.add_column("Max Speed", justify="center", style="green")

        i = 0
        for train, _ in self._model.train_positions.items():
            speed = str(round(train._speed, 2))
            max_speed = str(train._MAX_SPEED)
            if train._speed >= train._MAX_SPEED:
                max_speed += " max"

            table.add_row(str(i), speed, max_speed)
            i += 1

        return table

    def _generate_world_info_table(self) -> Table:
        table = Table(title="World")
        table.add_column("Sensor", justify="center", style="cyan")
        table.add_column("State", justify="center", style="green")
        table.add_row("1", "UP")

        return table

    def _calculate_cell_size(self) -> float:
        window_width, window_height = pygame.display.get_surface().get_size()
        rows = len(self._model._matrix)
        cols = len(self._model._matrix[0])

        max_cell_width = window_width / cols
        max_cell_height = window_height / rows

        return min(max_cell_width, max_cell_height)
