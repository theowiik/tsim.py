import pygame
from controller import Controller
from model import World
from view import View
import threading


def _model_thread(world: World) -> None:
    clock = pygame.time.Clock()

    while True:
        world.tick()
        clock.tick(5)


# TODO: move to view
def _draw_thread(view: View) -> None:
    clock = pygame.time.Clock()

    while True:
        view.draw()
        clock.tick(200)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("train-sim 2.0")

    world = World()
    view = View(world, screen)
    controller = Controller(world, view)

    # Start train thread
    m_thread = threading.Thread(target=_model_thread, args=(world,))
    m_thread.start()

    # Draw loop
    d_thread = threading.Thread(target=_draw_thread, args=(view,))
    d_thread.start()

    # while True:
    #     controller.handle_events()


if __name__ == "__main__":
    main()
