import pygame

class Train:
    movement_speed: float = 2.333
    x: float = 1.0
    y: float = 1.0

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def move(self) -> None:
        self.x += self.movement_speed


class View:
    def __init__(self, train, screen):
        self.train = train
        self.screen = screen

    def draw(self):
        pygame.draw.circle(
            self.screen,
            (33, 77, 44),
            (self.train.x, self.train.y),
            10
        )


class Controller:
    def __init__(self, train, view):
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
