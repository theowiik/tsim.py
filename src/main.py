import pygame
from controller import Controller
from model import Train
from view import View
import threading


def train_thread(train):
    clock = pygame.time.Clock()

    while True:
        train.move()
        clock.tick(10)


def draw_thread(view, controller, screen):
    clock = pygame.time.Clock()

    while True:
        controller.handle_events()

        # Draw
        screen.fill((0, 0, 0))
        view.draw()
        pygame.display.update()

        # Limit FPS
        clock.tick(200)


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("train-sim 2.0")

    train = Train(200, 200)
    view = View(train, screen)
    controller = Controller(train, view)

    # Start train thread
    t_thread = threading.Thread(target=train_thread, args=(train,))
    t_thread.start()

    # Draw loop
    d_thread = threading.Thread(
        target=draw_thread, args=(view, controller, screen, ))
    d_thread.start()


if __name__ == "__main__":
    main()
