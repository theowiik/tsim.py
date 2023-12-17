import pygame
from src.model import World


class Controller:
    def __init__(self, world: World, view):
        self.world = world
        self.view = view

    def handle_events(self):
        print("handling events")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Space key pressed")
