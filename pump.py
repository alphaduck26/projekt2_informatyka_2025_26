from drawable import Drawable

class Pump(Drawable):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas):
        canvas.create_oval(
            self.x - 12, self.y - 12,
            self.x + 12, self.y + 12,
            width=2
        )
        canvas.create_text(self.x, self.y, text="P")