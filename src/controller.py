import pygame
from model import World


class Controller:
    def __init__(self, world: World, view):
        self.world = world
        self.view = view

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.world.is_accelerating = not self.world.is_accelerating
