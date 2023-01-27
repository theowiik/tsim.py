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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] > self.train.x:
                    print('eee ooo eee ooo')
