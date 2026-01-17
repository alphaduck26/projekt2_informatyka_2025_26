from drawable import Drawable

class Pump(Drawable):
    def __init__(self, x, y):
        self.x, self.y = x, y

    def draw(self, canvas):
        canvas.create_oval(
            self.x - 15, self.y - 15,
            self.x + 15, self.y + 15,
            fill="#4444aa"
        )
        canvas.create_text(self.x, self.y + 25, text="Pompa", fill="white")