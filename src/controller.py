import pygame
from model import Train


class Controller:
    def __init__(self, train: Train, view):
        self.train = train
        self.view = view

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
