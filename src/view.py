import pygame
from pygame import Surface
from core.data import CellType, Direction, SwitchState
from model import World


class View:
    _CELL_WIDTH = 20
    _CELL_MARGIN = 2
    _CELL_NONE_COLOR = (136, 75, 75)
    _CELL_TRACK_COLOR = (136, 136, 75)
    _CELL_TRAIN_COLORS = [(75, 75, 136), (66, 123, 123)]
    _CLEAR_COLOR = (43, 42, 41)
    _CELL_TRAIN_CRASH_COLOR = (200, 20, 20)

    _SWITCH_LEFT_UP = "U"  # ┘
    _SWITCH_LEFT_DOWN = "D"  # ┐
    _SWITCH_RIGHT_UP = "U"  # └
    _SWITCH_RIGHT_DOWN = "D"  # ┌

    def __init__(self, world: World, screen: Surface):
        self._world = world
        self._screen = screen

    def draw(self) -> None:
        """
        Main draw function
        """
        self._screen.fill(self._CLEAR_COLOR)
        self._draw_matrix()
        self._draw_trains()
        pygame.display.update()

    def _draw_trains(self) -> None:
        # TODO: move to other draw function

        i = 0
        for train, positions in self._world.train_positions.items():
            for train_cell_index, position in enumerate(positions):
                xoffset = self._CELL_MARGIN + position[0] * (
                    self._CELL_WIDTH + self._CELL_MARGIN
                )

                yoffset = self._CELL_MARGIN + position[1] * (
                    self._CELL_WIDTH + self._CELL_MARGIN
                )

                train_color = self._CELL_TRAIN_COLORS[i % len(self._CELL_TRAIN_COLORS)]
                if train.state == "CRASHED":
                    train_color = self._CELL_TRAIN_CRASH_COLOR

                pygame.draw.rect(
                    self._screen,
                    train_color,
                    pygame.Rect(
                        xoffset + self._CELL_MARGIN,
                        yoffset + self._CELL_MARGIN,
                        self._CELL_WIDTH - self._CELL_MARGIN * 2,
                        self._CELL_WIDTH - self._CELL_MARGIN * 2,
                    ),
                )

                # Draw direction of train
                if train_cell_index == 0:
                    direction: str = self._get_direction_symbol(train.direction)
                    # font = pygame.font.Font(None, 36)
                    # text = font.render(direction, True, (0, 0, 0))
                    # self._screen.blit(
                    #     text, (xoffset + self._CELL_MARGIN, )
                    # )

                    self._render_text(
                        direction,
                        xoffset + self._CELL_MARGIN,
                        yoffset + self._CELL_MARGIN,
                    )

            i += 1

    def _render_text(self, text: str, x: int, y: int) -> None:
        font = pygame.font.Font(None, 36)
        text = font.render(text, True, (0, 0, 0))
        self._screen.blit(text, (x, y))

    def _get_direction_symbol(self, direction: Direction):
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

        for row in self._world._matrix:
            xoffset = self._CELL_MARGIN

            for cell in row:
                color = self._CELL_NONE_COLOR

                if cell.cell_type in [
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

                if cell.cell_type == CellType.SWITCH_LEFT:
                    if cell.switch_state == SwitchState.UP:
                        self._render_text(self._SWITCH_LEFT_UP, xoffset, yoffset)
                    elif cell.switch_state == SwitchState.DOWN:
                        self._render_text(self._SWITCH_LEFT_DOWN, xoffset, yoffset)
                    else:
                        self._render_text("!!", xoffset, yoffset)

                elif cell.cell_type == CellType.SWITCH_RIGHT:
                    if cell.switch_state == SwitchState.UP:
                        self._render_text(self._SWITCH_RIGHT_UP, xoffset, yoffset)
                    elif cell.switch_state == SwitchState.DOWN:
                        self._render_text(self._SWITCH_RIGHT_DOWN, xoffset, yoffset)
                    else:
                        self._render_text("!!", xoffset, yoffset)

                xoffset += self._CELL_WIDTH + self._CELL_MARGIN

            yoffset += self._CELL_WIDTH + self._CELL_MARGIN
