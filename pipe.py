from drawable import Drawable

class ThickPipe(Drawable):
    def __init__(self, offset=5, fill="#d0d0d0"):
        self.points = []
        self.offset = offset
        self.fill = fill

    def add_point(self, x, y):
        self.points.append((x, y))

    def draw(self, canvas):
        if len(self.points) < 2:
            return

        # odcinki
        for i in range(len(self.points) - 1):
            x1, y1 = self.points[i]
            x2, y2 = self.points[i + 1]

            if x1 == x2:  # pion
                canvas.create_rectangle(
                    x1 - self.offset, min(y1, y2),
                    x1 + self.offset, max(y1, y2),
                    fill=self.fill,
                    outline=""
                )

            elif y1 == y2:  # poziom
                canvas.create_rectangle(
                    min(x1, x2), y1 - self.offset,
                    max(x1, x2), y1 + self.offset,
                    fill=self.fill,
                    outline=""
                )

        # narożniki
        for i in range(1, len(self.points) - 1):
            x, y = self.points[i]
            canvas.create_rectangle(
                x - self.offset, y - self.offset,
                x + self.offset, y + self.offset,
                fill=self.fill,
                outline=""
            )