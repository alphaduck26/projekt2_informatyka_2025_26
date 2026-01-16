from drawable import Drawable

class Heater(Drawable):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas):
        canvas.create_text(
            self.x, self.y,
            text="🔥🔥🔥",
            font=("Arial", 16)
        )