from drawable import Drawable

def hex_to_rgb(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


class Tank(Drawable):
    def __init__(self, x, y, w, h, label, color,
                 level=0.0, is_filter=False, is_cooler=False):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.label = label

        self.color = color
        self.base_rgb = hex_to_rgb(color)   # ⭐ KLUCZOWE
        self.level = level

        self.animating = False
        self.is_filter = is_filter
        self.is_cooler = is_cooler

        self.filter_dirty = 0.0
        self.temperature = 20.0
        self.max_temp = 60.0

        self.flushing = False
        self.flush_t = 0.0
        self.flush_from = None
        self.flush_to = None

    # ================= RYSOWANIE =================

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

        canvas.create_text(
            self.x + self.w /6, self.y - 10,
            text=self.label, font=("Arial", 10, "bold")
        )

    # ================= KOLOR =================

    def get_color(self):
        if self.flushing:
            r = int(self.flush_from[0] * (1 - self.flush_t) + self.flush_to[0] * self.flush_t)
            g = int(self.flush_from[1] * (1 - self.flush_t) + self.flush_to[1] * self.flush_t)
            b = int(self.flush_from[2] * (1 - self.flush_t) + self.flush_to[2] * self.flush_t)
            return rgb_to_hex((r, g, b))

        if self.is_filter:
            d = self.filter_dirty
            r = int(self.base_rgb[0] * (1 - d) + 120 * d)
            g = int(self.base_rgb[1] * (1 - d) + 80 * d)
            b = int(self.base_rgb[2] * (1 - d) + 60 * d)
            return rgb_to_hex((r, g, b))

        if self.is_cooler:
            if self.temperature <= 30:
                return self.color  # CZYSTY kolor początkowy

            t = (self.temperature - 30) / (self.max_temp - 30)
            t = min(1.0, max(0.0, t))

            r = int(self.base_rgb[0] * (1 - t) + 255 * t)
            g = int(self.base_rgb[1] * (1 - t))
            b = int(self.base_rgb[2] * (1 - t))
            return rgb_to_hex((r, g, b))


        return self.color

    # ================= ANIMACJA =================

    def start_flush(self):
        if self.flushing:
            return
        self.flush_from = hex_to_rgb(self.get_color())
        self.flush_to = self.base_rgb
        self.flush_t = 0.0
        self.flushing = True

    def update_flush(self):
        if not self.flushing:
            return
        self.flush_t += 0.03
        if self.flush_t >= 1.0:
            self.flush_t = 1.0
            self.flushing = False
            self.filter_dirty = 0.0
            self.temperature = 20.0

    # ================= OBJĘTOŚĆ =================

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

    # ================= LOGIKA =================

    def remove_volume(self, v):
        self.level = max(0, self.level - v)

    def add_volume(self, v):
        self.level = min(1.0, self.level + v)

    def filter(self, vapor):
        if self.flushing or not self.is_filter or self.filter_dirty >= 1:
            return 0.0
        passed = vapor * (1.0 - self.filter_dirty)
        self.filter_dirty += vapor * 0.5
        self.filter_dirty = min(1.0, self.filter_dirty)
        return passed

    def reset_filter(self):
        self.start_flush()

    def condense(self, vapor):
        if self.flushing or not self.is_cooler or self.temperature >= self.max_temp:
            return 0.0
        condensed = min(vapor, 0.003)
        self.temperature += condensed * 50
        return condensed

    def cool_down(self):
        self.start_flush()
