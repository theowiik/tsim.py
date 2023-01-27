import pygame
from model import Train


class View:
    def __init__(self, train: Train, screen):
        self.train = train
        self.screen = screen

    def draw(self):
        pygame.draw.circle(
            self.screen,
            (33, 77, 44),
            (self.train.x, self.train.y),
            10
        )
