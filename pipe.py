from drawable import Drawable

class ThickPipe(Drawable):
    def __init__(self, offset=3, width=3):
        self.segments = []
        self.offset = offset
        self.width = width

    def add(self, x1, y1, x2, y2):
        self.segments.append((x1, y1, x2, y2))

    def draw(self, canvas):
        for x1, y1, x2, y2 in self.segments:
            if x1 == x2:  # pion
                canvas.create_line(x1 - self.offset, y1, x2 - self.offset, y2, width=self.width)
                canvas.create_line(x1 + self.offset, y1, x2 + self.offset, y2, width=self.width)
            else:         # poziom
                canvas.create_line(x1, y1 - self.offset, x2, y2 - self.offset, width=self.width)
                canvas.create_line(x1, y1 + self.offset, x2, y2 + self.offset, width=self.width)