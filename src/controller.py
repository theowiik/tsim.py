import threading

import pygame

from model import Model
from view import View


class Controller:
    _TPS: int = 10
    _FPS: int = 60

    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view

    def start(self) -> None:
        m_thread = threading.Thread(target=self._model_thread, args=())
        m_thread.start()

        # Draw loop
        d_thread = threading.Thread(target=self._draw_thread, args=())
        d_thread.start()

        while True:
            self._handle_events()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.model.is_accelerating = not self.model.is_accelerating

    def _model_thread(self) -> None:
        clock = pygame.time.Clock()

        while True:
            self.model.tick()
            clock.tick(self._TPS)

    def _draw_thread(self) -> None:
        clock = pygame.time.Clock()

        while True:
            self.view.draw()
            clock.tick(self._FPS)  # TODO: unsure if this is correct
