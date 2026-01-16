from drawable import Drawable
from pipe import ThickPipe

class CoilPipe(Drawable):
    def __init__(self, x, y, height, loops=6, width=50):
        self.pipe = ThickPipe()

        step = height // loops
        cx, cy = x, y
        self.pipe.add_point(cx, cy)

        direction = -1
        for _ in range(loops):
            cx += direction * width
            self.pipe.add_point(cx, cy)

            cy += step
            self.pipe.add_point(cx, cy)

            direction *= -1

    def draw(self, canvas):
        self.pipe.draw(canvas)