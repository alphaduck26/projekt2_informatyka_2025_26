from drawable import Drawable

class Heater(Drawable):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.on = False
        self.target = 50
        self.current_temp = 50

    def toggle(self):
        self.on = not self.on

    def set_target(self, t):
        self.target = t

    def update(self):
        if self.on:
            self.current_temp += (self.target - self.current_temp) * 0.1
        else:
            self.current_temp += (20 - self.current_temp) * 0.05

    def draw(self, canvas):
        t = max(0, min(1, (self.current_temp - 50) / 40))
        r = int(255 * t)
        canvas.create_rectangle(
            self.x - 20, self.y,
            self.x + 20, self.y + 20,
            fill=f"#{r:02x}0000", outline="black"
        )
        canvas.create_text(self.x, self.y + 35, text=f"{int(self.current_temp)}°C")