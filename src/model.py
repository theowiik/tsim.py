class Train:
    movement_speed: float = 2.333
    x: float = 1.0
    y: float = 1.0

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def move(self) -> None:
        self.x += self.movement_speed
