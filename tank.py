from drawable import Drawable


class Tank(Drawable):
    def __init__(self, x, y, w, h, label):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.label = label

        self.level = 0.0   # 0–1
        self.anim_id = 0

        if "Braga" in label:
            self.content_color = "#5F9EA0"
        elif "Filtr" in label or "Chłodnica" in label:
            self.content_color = "#8fd3ff"
        elif "Produkt" in label:
            self.content_color = "#7FFFD4"
        else:
            self.content_color = None

    def draw(self, canvas):
        if self.content_color and self.level > 0:
            fill_height = self.h * self.level
            canvas.create_rectangle(
                self.x + 3,
                self.y + self.h - fill_height,
                self.x + self.w - 3,
                self.y + self.h - 3,
                fill=self.content_color,
                outline=""
            )

        canvas.create_rectangle(
            self.x, self.y,
            self.x + self.w,
            self.y + self.h,
            outline="black",
            width=2
        )

        canvas.create_text(
            self.x + self.w / 6,
            self.y - 10,
            text=self.label,
            font=("Arial", 10, "bold")
        )

    # ===== ANIMACJE =====

    def fill_to(self, canvas, redraw_cb, target=0.9, duration=6000):
        self.anim_id += 1
        current_id = self.anim_id

        steps = max(1, int(duration / 50))
        delta = (target - self.level) / steps

        def step():
            if current_id != self.anim_id:
                return

            if abs(self.level - target) <= abs(delta):
                self.level = target
                redraw_cb(canvas)
                return

            self.level += delta
            canvas.delete("all")
            redraw_cb(canvas)
            canvas.after(50, step)

        step()

    def empty(self, canvas, redraw_cb, duration=4000):
        self.anim_id += 1
        current_id = self.anim_id

        steps = max(1, int(duration / 50))
        delta = self.level / steps

        def step():
            if current_id != self.anim_id:
                return

            if self.level <= 0:
                self.level = 0.0
                redraw_cb(canvas)
                return

            self.level -= delta
            if self.level < 0:
                self.level = 0.0

            canvas.delete("all")
            redraw_cb(canvas)
            canvas.after(50, step)

        step()

    # ===== PROCES =====

    def remove_volume(self, amount):
        self.level -= amount
        if self.level < 0:
            self.level = 0.0