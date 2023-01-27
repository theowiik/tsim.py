import pygame
from controller import Controller
from model import Train
from view import View


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("train-sim 2.0")

    train = Train(1, 1)
    view = View(train, screen)
    controller = Controller(train, view)

    running = True
    while running:
        screen.fill((255, 255, 255))
        controller.handle_events()
        train.move()
        view.draw()
        pygame.display.update()

        # wait 1/60th of a second
        pygame.time.delay(16)


if __name__ == "__main__":
    main()
