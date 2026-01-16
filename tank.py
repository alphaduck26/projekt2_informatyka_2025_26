from drawable import Drawable


class Tank(Drawable):
    def __init__(self, x, y, w, h, label):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.label = label

        self.level = 0.0
        self.anim_id = 0  # identyfikator animacji

        # FILTR
        self.is_filter = "Filtr" in label
        self.dirt = 0.0
        self.blocked = False

        if "Braga" in label:
            self.base_color = "#5F9EA0"
        elif self.is_filter:
            self.base_color = "#8fd3ff"
        elif "Chłodnica" in label:
            self.base_color = "#8fd3ff"
        elif "Produkt" in label:
            self.base_color = "#7FFFD4"
        else:
            self.base_color = None

    # ================= KOLORY =================

    def liquid_color(self):
        if not self.is_filter:
            return self.base_color

        # interpolacja koloru filtra (czysty → brudny)
        r = int(0x8f + self.dirt * (0x55 - 0x8f))
        g = int(0xd3 + self.dirt * (0x30 - 0xd3))
        b = int(0xff + self.dirt * (0x10 - 0xff))
        return f"#{r:02x}{g:02x}{b:02x}"

    # ================= RYSOWANIE =================

    def draw(self, canvas):
        if self.level > 0:
            fill_height = self.h * self.level
            canvas.create_rectangle(
                self.x + 3,
                self.y + self.h - fill_height,
                self.x + self.w - 3,
                self.y + self.h - 3,
                fill=self.liquid_color(),
                outline=""
            )

        canvas.create_rectangle(
            self.x, self.y,
            self.x + self.w,
            self.y + self.h,
            outline="black",
            width=3 if self.blocked else 2
        )

        canvas.create_text(
            self.x + self.w / 6,
            self.y - 10,
            text=self.label,
            font=("Arial", 10, "bold")
        )

        if self.is_filter and self.blocked:
            canvas.create_text(
                self.x + self.w / 2,
                self.y + self.h / 2,
                text="ZATKANY",
                fill="red",
                font=("Arial", 10, "bold")
            )

    # ================= ANIMACJE =================

    def fill_to(self, canvas, redraw, target=0.9, duration=6000):
        self.anim_id += 1
        current_id = self.anim_id

        steps = max(1, duration // 50)
        delta = (target - self.level) / steps

        def step():
            if current_id != self.anim_id:
                return

            if (delta > 0 and self.level >= target) or \
               (delta < 0 and self.level <= target):
                self.level = max(0.0, min(1.0, target))
                redraw()
                return

            self.level += delta
            self.level = max(0.0, min(1.0, self.level))
            redraw()
            canvas.after(50, step)

        step()

    def empty(self, canvas, redraw, duration=4000):
        self.fill_to(canvas, redraw, target=0.0, duration=duration)

    # ================= PROCES =================

    def remove_volume(self, amount):
        self.level = max(0.0, self.level - amount)

    def add_dirt(self, amount):
        if not self.blocked:
            self.dirt += amount
            if self.dirt >= 1.0:
                self.dirt = 1.0
                self.blocked = True

    def reset_filter(self):
        self.level = 0.4
        self.dirt = 0.0
        self.blocked = False
