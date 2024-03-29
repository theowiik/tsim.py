from tsimpy.model import Model


class TSimPyInterface:
    def __init__(self, model: Model):
        self.model = model

    def do_action() -> None:
        print("Doing action")
