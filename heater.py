from drawable import Drawable

class Heater(Drawable):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas):
        canvas.create_rectangle(
            self.x - 20, self.y,
            self.x + 20, self.y + 20,
            fill="#cc3300",
            outline=""
        )

        canvas.create_text(
            self.x, self.y + 30,
            text="Piec",
            fill="white"
        )