import pygame
from model import Train

train_color = (66, 245, 158)


class View:
    def __init__(self, train: Train, screen):
        self.train = train
        self.screen = screen

    def draw(self):
        pygame.draw.rect(
            self.screen,
            train_color,
            pygame.Rect(
                self.train.x,
                self.train.y,
                self.train.cargo_length,
                20,
            ),
        )
