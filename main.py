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

T2.level = 0.4  # filtr zalany wodą

elements += [T1, T2, T3, T4]

# ================= PIEC =================
heater = Heater(820, 340)
elements.append(heater)

# ================= RURY (BEZ ZMIAN) =================
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

# ================= PARA =================

path_T1_T2 = [(820,220),(820,180),(620,180),(620,200)]
path_T2_T3 = [(560,230),(410,230)]

def path_len(p):
    return sum(math.hypot(p[i+1][0]-p[i][0], p[i+1][1]-p[i][1])
               for i in range(len(p)-1))

class Vapor:
    def __init__(self, path):
        self.path = path
        self.total = path_len(path)
        self.pos = 0.0
        self.speed = 6

    def update(self):
        self.pos += self.speed
        return self.pos >= self.total

    def draw(self, canvas):
        d = self.pos
        for i in range(len(self.path)-1):
            a, b = self.path[i], self.path[i+1]
            seg = math.hypot(b[0]-a[0], b[1]-a[1])
            if d <= seg:
                t = d/seg if seg else 0
                x = a[0]+(b[0]-a[0])*t
                y = a[1]+(b[1]-a[1])*t
                canvas.create_oval(x-4,y-4,x+4,y+4,fill="#eeeeee",outline="")
                return
            d -= seg

vapors_T2 = []
vapors_T3 = []

# ================= LOGIKA =================

def redraw():
    canvas.delete("all")
    for e in elements:
        e.draw(canvas)
    for v in vapors_T2 + vapors_T3:
        v.draw(canvas)

def process_loop():
    heater.update()

    # PAROWANIE
    if T1.level > 0 and heater.current_temp > 60:
        rate = (heater.current_temp - 60) / 30
        rate = max(0, min(1, rate))
        evap = 0.001 * rate

        T1.remove_volume(evap)

        for _ in range(int(evap * 4000)):
            vapors_T2.append(Vapor(path_T1_T2))

    # T1 -> T2
    for v in vapors_T2[:]:
        if v.update():
            vapors_T2.remove(v)
            if not T2.blocked:
                T2.add_dirt(0.002)
                vapors_T3.append(Vapor(path_T2_T3))

    # T2 -> T3
    for v in vapors_T3[:]:
        if v.update():
            vapors_T3.remove(v)
            # (skraplanie później)

    redraw()
    root.after(100, process_loop)

# ================= UI =================

tk.Label(ui, text="T1 – Braga", font=("Arial", 12, "bold")).pack(pady=5)
tk.Button(ui, text="Uzupełnij",
          command=lambda: T1.fill_to(canvas, redraw, 0.9, 6000)).pack(fill="x")
tk.Button(ui, text="Opróżnij",
          command=lambda: T1.empty(canvas, redraw)).pack(fill="x", pady=5)

tk.Label(ui, text="Filtr", font=("Arial", 12, "bold")).pack(pady=10)
tk.Button(ui, text="Wymień filtr",
          command=lambda: T2.reset_filter()).pack(fill="x")

tk.Label(ui, text="Piec", font=("Arial", 12, "bold")).pack(pady=10)
tk.Button(ui, text="ON / OFF",
          command=lambda: heater.toggle()).pack(fill="x")

tk.Scale(ui, from_=50, to=90, orient="horizontal",
         command=lambda v: heater.set_temp_value(int(v))).pack(fill="x")

process_loop()
root.mainloop()