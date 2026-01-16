from drawable import Drawable


class Heater(Drawable):
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.on = False

        self.set_temp = 50        # temperatura zadana
        self.current_temp = 50.0  # temperatura rzeczywista

        self.inertia = 0.02       # współczynnik bezwładności

        self.body_tag = "heater_body"
        self.text_tag = "heater_temp"

    def set_temp_value(self, temp):
        self.set_temp = temp

    def toggle(self):
        self.on = not self.on

    def update(self):
        """Symulacja bezwładności cieplnej"""
        target = self.set_temp if self.on else 20  # stygnie do otoczenia

        delta = target - self.current_temp
        self.current_temp += delta * self.inertia

    def color(self):
        if not self.on:
            return "#555555"

        t = (self.current_temp - 50) / 40
        t = max(0.0, min(1.0, t))
        r = int(255 * t)
        return f"#{r:02x}0000"

    def draw(self, canvas):
        canvas.delete(self.body_tag)
        canvas.delete(self.text_tag)

        canvas.create_rectangle(
            self.x - 20,
            self.y,
            self.x + 20,
            self.y + 20,
            fill=self.color(),
            outline="black",
            tags=self.body_tag
        )

        canvas.create_text(
            self.x,
            self.y + 35,
            text=f"{int(self.current_temp)}°C",
            tags=self.text_tag
        )