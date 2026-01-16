import tkinter as tk
import math

from tank import Tank
from heater import Heater
from pump import Pump
from pipe import ThickPipe
from coil import CoilPipe

root = tk.Tk()
root.title("SCADA – Destylator")

canvas = tk.Canvas(root, width=1000, height=500, bg="#A5B272")
canvas.pack(side=tk.LEFT)

ui = tk.Frame(root)
ui.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

elements = []

# ================= ZBIORNIKI =================
T1 = Tank(760, 220, 120, 100, "T1 - Braga")
T2 = Tank(560, 200, 120, 60, "T2 - Filtr")
T3 = Tank(330, 200, 120, 220, "T3 - Chłodnica")
T4 = Tank(80, 370, 120, 80, "T4 - Produkt")

elements += [T1, T2, T3, T4]

# ================= PIEC =================
heater = Heater(820, 340)
elements.append(heater)

# ================= RURY =================
pipe_in = ThickPipe()
pipe_in.add_point(820, 220)
pipe_in.add_point(820, 180)
pipe_in.add_point(620, 180)
pipe_in.add_point(620, 200)
elements.append(pipe_in)

pipe_out_t2 = ThickPipe()
pipe_out_t2.add_point(560, 230)
pipe_out_t2.add_point(410, 230)
elements.append(pipe_out_t2)

coil = CoilPipe(410, 230, 160, 6)
elements.append(coil)

pipe_product = ThickPipe(fill="#d0d0d0")
pipe_product.add_point(415, 381)
pipe_product.add_point(180, 381)
elements.append(pipe_product)

cold_in = ThickPipe(offset=4, fill="#8fd3ff")
cold_in.add_point(330, 240)
cold_in.add_point(290, 240)
elements.append(cold_in)

hot_out = ThickPipe(offset=4, fill="#ffb347")
hot_out.add_point(330, 360)
hot_out.add_point(290, 360)
elements.append(hot_out)

elements.append(Pump(300, 300))

# ================= MODEL PARY =================

# Trasa pary (dokładnie po rurze T1 -> T2)
vapor_path = [
    (820, 220),
    (820, 180),
    (620, 180),
    (620, 200),
]

def segment_length(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])

path_lengths = [segment_length(vapor_path[i], vapor_path[i+1])
                for i in range(len(vapor_path)-1)]
path_total = sum(path_lengths)


class VaporParticle:
    def __init__(self):
        self.pos = 0.0  # 0–1 wzdłuż całej trasy
        self.speed = 0.01

    def update(self):
        self.pos += self.speed
        return self.pos >= 1.0

    def draw(self, canvas):
        d = self.pos * path_total
        for i, seg_len in enumerate(path_lengths):
            if d <= seg_len:
                a = vapor_path[i]
                b = vapor_path[i+1]
                t = d / seg_len if seg_len > 0 else 0
                x = a[0] + (b[0] - a[0]) * t
                y = a[1] + (b[1] - a[1]) * t
                canvas.create_oval(
                    x-4, y-4, x+4, y+4,
                    fill="#eeeeee", outline=""
                )
                return
            d -= seg_len


vapors = []

# ================= PETLA PROCESU =================

def redraw(canvas):
    canvas.delete("all")
    for e in elements:
        e.draw(canvas)
    for v in vapors:
        v.draw(canvas)


def process_loop():
    heater.update()

    # ===== PAROWANIE =====
    if T1.level > 0 and heater.current_temp > 60:
        temp_factor = (heater.current_temp - 60) / 30
        temp_factor = max(0.0, min(1.0, temp_factor))

        evaporation_rate = 0.0003 + temp_factor * 0.002

        T1.remove_volume(evaporation_rate)

        # 1 jednostka bragi -> 5 jednostek pary
        vapor_units = int(evaporation_rate * 5000)
        for _ in range(vapor_units):
            vapors.append(VaporParticle())

    # ===== TRANSPORT PARY =====
    finished = []
    for v in vapors:
        if v.update():
            finished.append(v)
            T2.level = min(1.0, T2.level + 0.002)

    for v in finished:
        vapors.remove(v)

    redraw(canvas)
    root.after(100, process_loop)

# ================= UI =================

tk.Label(ui, text="T1 – Braga", font=("Arial", 12, "bold")).pack(pady=5)

tk.Button(
    ui,
    text="Uzupełnij",
    command=lambda: T1.fill_to(canvas, redraw, 0.9, 6000)
).pack(fill="x")

tk.Button(
    ui,
    text="Opróżnij",
    command=lambda: T1.empty(canvas, redraw)
).pack(fill="x", pady=5)

tk.Label(ui, text="Piec", font=("Arial", 12, "bold")).pack(pady=10)

tk.Button(
    ui,
    text="ON / OFF",
    command=lambda: heater.toggle()
).pack(fill="x")

temp_slider = tk.Scale(
    ui,
    from_=50,
    to=90,
    orient="horizontal",
    command=lambda v: heater.set_temp_value(int(v))
)
temp_slider.set(50)
temp_slider.pack(fill="x")

process_loop()
root.mainloop()