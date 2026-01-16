import tkinter as tk

from tank import Tank
from heater import Heater
from pump import Pump
from pipe import ThickPipe
from coil import CoilPipe

root = tk.Tk()
root.title("SCADA – Destylator")

canvas = tk.Canvas(
    root,
    width=1000,
    height=500,
    bg="#A5B272"
)
canvas.pack()

elements = []

# ZBIORNIKI (od prawej)
T1 = Tank(760, 220, 120, 100, "T1 - Braga")
T2 = Tank(560, 200, 120, 60, "T2 - Filtr")
T3 = Tank(330, 200, 120, 220, "T3 - Chłodnica")
T4 = Tank(80, 370, 120, 80, "T4 - Produkt")

elements += [T1, T2, T3, T4]

# GRZAŁKA
elements.append(Heater(820, 340))

# RURA PAROWA T1 → T2 → T3
pipe = ThickPipe()
pipe.add_point(820, 220)
pipe.add_point(820, 180)
pipe.add_point(620, 180)
pipe.add_point(620, 220)
pipe.add_point(410, 220)
elements.append(pipe)

# WĘŻOWNICA
coil = CoilPipe(
    x=410,
    y=220,
    height=160,
    loops=6
)
elements.append(coil)

# WYJŚCIE DO T4
pipe_out = ThickPipe()
pipe_out.add_point(415, 380)
pipe_out.add_point(180, 380)
elements.append(pipe_out)

# RURY WODY CHŁODZĄCEJ (T3)
cold_in = ThickPipe(offset=4, fill="#8fd3ff")
cold_in.add_point(330, 240)
cold_in.add_point(290, 240)
elements.append(cold_in)

hot_out = ThickPipe(offset=4, fill="#ffb347")
hot_out.add_point(330, 360)
hot_out.add_point(290, 360)
elements.append(hot_out)

# POMPA
elements.append(Pump(300, 300))

# RYSOWANIE
for e in elements:
    e.draw(canvas)

root.mainloop()