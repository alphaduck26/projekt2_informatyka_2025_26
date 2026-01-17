from drawable import Drawable

class Tank(Drawable):
    def __init__(self, x, y, w, h, label, color,
                 level=0.0, is_filter=False, is_cooler=False):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.label = label
        self.color = color
        self.level = level

        self.animating = False
        self.is_filter = is_filter
        self.is_cooler = is_cooler

        self.filter_dirty = 0.0
        self.temperature = 20.0
        self.max_temp = 60.0

    def draw(self, canvas):
        if self.level > 0:
            fh = self.h * self.level
            canvas.create_rectangle(
                self.x + 3, self.y + self.h - fh,
                self.x + self.w - 3, self.y + self.h - 3,
                fill=self.get_color(), outline=""
            )

        canvas.create_rectangle(
            self.x, self.y,
            self.x + self.w, self.y + self.h,
            outline="black", width=2
        )

        canvas.create_text(self.x + self.w / 2, self.y - 10,
                           text=self.label, font=("Arial", 10, "bold"))

    def get_color(self):
        if self.is_filter:
            d = self.filter_dirty
            r = int(120 + d * 80)
            g = int(200 - d * 120)
            b = int(120 - d * 100)
            return f"#{r:02x}{g:02x}{b:02x}"

        if self.is_cooler:
            t = min(1.0, self.temperature / self.max_temp)
            r = int(255 * t)
            g = int(200 * (1 - t))
            b = int(255 * (1 - t))
            return f"#{r:02x}{g:02x}{b:02x}"

        return self.color

    def fill_to(self, canvas, redraw, target, duration):
        if self.animating:
            return
        self.animating = True
        steps = duration // 50
        delta = (target - self.level) / steps

        def step():
            if abs(self.level - target) < abs(delta):
                self.level = target
                self.animating = False
                redraw()
                return
            self.level += delta
            redraw()
            canvas.after(50, step)

        step()

    def empty(self, canvas, redraw):
        if self.animating:
            return
        self.animating = True

        def step():
            if self.level <= 0:
                self.level = 0
                self.animating = False
                redraw()
                return
            self.level -= 0.01
            redraw()
            canvas.after(50, step)

        step()

    def remove_volume(self, v):
        self.level = max(0, self.level - v)

    def add_volume(self, v):
        self.level = min(1.0, self.level + v)

    def filter(self, vapor):
        if not self.is_filter or self.filter_dirty >= 1:
            return 0.0
        efficiency = 1.0 - self.filter_dirty
        passed = vapor * efficiency
        self.filter_dirty += vapor * 2
        self.filter_dirty = min(1.0, self.filter_dirty)
        return passed

    def reset_filter(self):
        self.filter_dirty = 0.0
        self.level = 0.4

    def condense(self, vapor):
        if not self.is_cooler or self.temperature >= self.max_temp:
            return 0.0
        condensed = min(vapor, 0.003)
        self.temperature += condensed * 50
        return condensed

    def cool_down(self):
        self.temperature = 20.0 