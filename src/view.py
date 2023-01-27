import pygame
from model import World

train_color = (66, 245, 158)


class View:
    def __init__(self, world: World, screen):
        self.world = world
        self.screen = screen

    def draw(self):
        for train in self.world.trains:
            pygame.draw.rect(
                self.screen,
                train_color,
                pygame.Rect(
                    train.x,
                    train.y,
                    train.cargo_length,
                    20,
                ),
            )
