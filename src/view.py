import pygame
from pygame import Surface
from core.data import CellType, Direction
from model import World


class View:
    CELL_WIDTH = 40
    CELL_MARGIN = 5
    CELL_NONE_COLOR = (136, 75, 75)
    CELL_TRACK_COLOR = (136, 136, 75)
    CELL_TRAIN_COLOR = [(75, 75, 136), (66, 123, 123)]
    CLEAR_COLOR = (43, 42, 41)
    CELL_TRAIN_CRASH_COLOR = (200, 20, 20)

    def __init__(self, world: World, screen: Surface):
        self.world = world
        self.screen = screen

    def draw(self) -> None:
        """
        Main draw function
        """
        self.screen.fill(self.CLEAR_COLOR)
        self._draw_matrix()
        self._draw_trains()
        pygame.display.update()

    def _draw_trains(self) -> None:
        i = 0
        for train, positions in self.world.train_positions.items():
            for train_cell_index, position in enumerate(positions):
                xoffset = self.CELL_MARGIN + position[0] * (
                    self.CELL_WIDTH + self.CELL_MARGIN
                )

                yoffset = self.CELL_MARGIN + position[1] * (
                    self.CELL_WIDTH + self.CELL_MARGIN
                )

                train_color = self.CELL_TRAIN_COLOR[i % len(self.CELL_TRAIN_COLOR)]
                if train._state == "CRASHED":
                    train_color = self.CELL_TRAIN_CRASH_COLOR

                pygame.draw.rect(
                    self.screen,
                    train_color,
                    pygame.Rect(
                        xoffset + self.CELL_MARGIN,
                        yoffset + self.CELL_MARGIN,
                        self.CELL_WIDTH - self.CELL_MARGIN * 2,
                        self.CELL_WIDTH - self.CELL_MARGIN * 2,
                    ),
                )

                # Draw direction of train
                if train_cell_index == 0:
                    direction: str = self._get_direction_symbol(train.direction)
                    font = pygame.font.Font(None, 36)
                    text = font.render(direction, True, (0, 0, 0))
                    self.screen.blit(
                        text, (xoffset + self.CELL_MARGIN, yoffset + self.CELL_MARGIN)
                    )

            i += 1

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
        yoffset = self.CELL_MARGIN

        for row in self.world._matrix:
            xoffset = self.CELL_MARGIN

            for cell in row:
                color = self.CELL_NONE_COLOR

                if cell.cell_type == CellType.TRACK:
                    color = self.CELL_TRACK_COLOR

                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(
                        xoffset,
                        yoffset,
                        self.CELL_WIDTH,
                        self.CELL_WIDTH,
                    ),
                )

                xoffset += self.CELL_WIDTH + self.CELL_MARGIN

            yoffset += self.CELL_WIDTH + self.CELL_MARGIN
