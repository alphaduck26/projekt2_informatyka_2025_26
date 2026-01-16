from drawable import Drawable

class Tank(Drawable):
    def __init__(self, x, y, w, h, label):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.label = label

    def draw(self, canvas):
        canvas.create_rectangle(
            self.x, self.y,
            self.x + self.w, self.y + self.h,
            fill="#6f8f3f",
            outline=""
        )

        canvas.create_text(
            self.x + self.w / 5,
            self.y - 10,
            text=self.label,
            fill="white"
        )