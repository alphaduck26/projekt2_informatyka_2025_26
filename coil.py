from drawable import Drawable

class CoilPipe(Drawable):
    def __init__(self, x, y, height, loops=6, width=50, offset=5):
        self.x = x
        self.y = y
        self.height = height
        self.loops = loops
        self.width = width
        self.offset = offset

    def draw(self, canvas):
        step = self.height // self.loops
        x = self.x
        y = self.y
        direction = -1

        for _ in range(self.loops):
            x2 = x + direction * self.width
            y2 = y + step

            canvas.create_line(x - self.offset, y, x2 - self.offset, y2, width=3)
            canvas.create_line(x + self.offset, y, x2 + self.offset, y2, width=3)

            x = x2
            y = y2
            direction *= -1