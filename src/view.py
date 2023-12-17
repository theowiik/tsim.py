import pygame
from pygame import Surface
from model import CellType, World


class View:
    CELl_WIDTH = 40
    CELL_MARGIN = 5
    CELL_NONE_COLOR = (136, 75, 75)
    CELL_TRACK_COLOR = (136, 136, 75)
    CELL_TRAIN_COLOR = [(75, 75, 136), (66, 123, 123)]
    CLEAR_COLOR = (43, 42, 41)

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
            for position in positions:
                xoffset = self.CELL_MARGIN + position[0] * (
                    self.CELl_WIDTH + self.CELL_MARGIN
                )

                yoffset = self.CELL_MARGIN + position[1] * (
                    self.CELl_WIDTH + self.CELL_MARGIN
                )

                train_color = self.CELL_TRAIN_COLOR[i % len(self.CELL_TRAIN_COLOR)]
                if train.state == "CRASHED":
                    train_color = (200, 20, 20)

                pygame.draw.rect(
                    self.screen,
                    train_color,
                    pygame.Rect(
                        xoffset + self.CELL_MARGIN,
                        yoffset + self.CELL_MARGIN,
                        self.CELl_WIDTH - self.CELL_MARGIN * 2,
                        self.CELl_WIDTH - self.CELL_MARGIN * 2,
                    ),
                )

            i += 1

    def _draw_matrix(self) -> None:
        yoffset = self.CELL_MARGIN

        for row in self.world.matrix:
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
                        self.CELl_WIDTH,
                        self.CELl_WIDTH,
                    ),
                )

                xoffset += self.CELl_WIDTH + self.CELL_MARGIN

            yoffset += self.CELl_WIDTH + self.CELL_MARGIN
