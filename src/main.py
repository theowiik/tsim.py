import pygame
from controller import Controller
from model import Train
from view import View
import threading


def train_thread(train):
    print('Starting train thread')
    print('Train thread id:', threading.get_ident())

    wait_time = 16  # milliseconds
    time_waited = pygame.time.get_ticks()

    while True:
        if pygame.time.get_ticks() - time_waited > wait_time:
            train.move()
            time_waited = pygame.time.get_ticks()


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
    clock = pygame.time.Clock()
    while True:
        controller.handle_events()

        # Draw
        print('Drawing 🖌️')
        screen.fill((0, 0, 0))
        view.draw()
        pygame.display.update()

        # Limit FPS
        clock.tick(200)


if __name__ == "__main__":
    main()
