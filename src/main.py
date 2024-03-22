import pygame

from controller import Controller
from model import Model
from view import View


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("train-sim 2.0")

    model = Model()
    view = View(model, screen)
    controller = Controller(model, view)

    controller.start()


if __name__ == "__main__":
    main()
