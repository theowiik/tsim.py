import pygame
from model import CellType, World


class View:
    cell_width = 40
    cell_margin = 5
    cell_none_color = (136, 75, 75)
    cell_track_color = (136, 136, 75)
    cell_train_colors = [(75, 75, 136), (66, 123, 123)]

    def __init__(self, world: World, screen):
        self.world = world
        self.screen = screen

    def draw(self):
        self.draw_matrix()
        self.draw_trains()

    def draw_trains(self):
        i = 0
        for train, positions in self.world.train_positions.items():
            for position in positions:
                xoffset = self.cell_margin + position[0] * (
                    self.cell_width + self.cell_margin
                )

                yoffset = self.cell_margin + position[1] * (
                    self.cell_width + self.cell_margin
                )

                train_color = self.cell_train_colors[i % len(self.cell_train_colors)]
                if train.state == "CRASHED":
                    train_color = (200, 20, 20)

                pygame.draw.rect(
                    self.screen,
                    train_color,
                    pygame.Rect(
                        xoffset + self.cell_margin,
                        yoffset + self.cell_margin,
                        self.cell_width - self.cell_margin * 2,
                        self.cell_width - self.cell_margin * 2,
                    ),
                )

            i += 1

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

                xoffset += self.cell_width + self.cell_margin

            yoffset += self.cell_width + self.cell_margin
