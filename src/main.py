import pygame

from tsimpy.controller import Controller
from tsimpy.model import Model
from tsimpy.tsimpyinterface import TSimPyInterface
from tsimpy.view import View


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("tsim.py")

    model = Model()
    view = View(model, screen)
    controller = Controller(model, view)

    controller.start()

    controller(TSimPyInterface(model))


def controller(model: TSimPyInterface) -> None:
    # ============ YOUR CODE HERE ============
    # TODO: Move to separate file

    pass


if __name__ == "__main__":
    main()
