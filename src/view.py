import pygame
from model import CellType, World


class View:
    cell_width = 40
    cell_margin = 5
    cell_none_color = (136, 75, 75)
    cell_track_color = (136, 136, 75)
    cell_train_color = (75, 75, 136)

    def __init__(self, world: World, screen):
        self.world = world
        self.screen = screen

    def draw(self):
        self.draw_matrix()

        for train in self.world.trains:
            pygame.draw.rect(
                self.screen,
                self.cell_train_color,
                pygame.Rect(
                    train.x,
                    train.y,
                    train.cargo_length,
                    20,
                ),
            )

    def draw_matrix(self):
        yoffset = self.cell_margin

        for row in self.world.matrix:
            xoffset = self.cell_margin

            for cell in row:
                color = self.cell_none_color

                if cell.cell_type == CellType.TRACK:
                    color = self.cell_track_color

                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(
                        xoffset,
                        yoffset,
                        self.cell_width,
                        self.cell_width,
                    ),
                )

                if cell.has_train:
                    pygame.draw.rect(
                        self.screen,
                        self.cell_train_color,
                        pygame.Rect(
                            xoffset + self.cell_margin,
                            yoffset + self.cell_margin,
                            self.cell_width - self.cell_margin * 2,
                            self.cell_width - self.cell_margin * 2,
                        ),
                    )

                xoffset += self.cell_width + self.cell_margin

            yoffset += self.cell_width + self.cell_margin
