import tkinter as tk

from tank import Tank
from heater import Heater
from pump import Pump
from pipe import ThickPipe
from coil import CoilPipe

root = tk.Tk()
root.title("SCADA - Destylator")
canvas = tk.Canvas(root, width=1000, height=500, bg="white")
canvas.pack()

elements = []

# ZBIORNIKI (jak na rysunku: od prawej)
T1 = Tank(760, 220, 120, 100, "T1 - Braga")
T2 = Tank(560, 200, 120, 60, "T2 - Filtr") #prawo, dol, szerokosc (w prawo), wysokosc (w dol) 
T3 = Tank(330, 200, 140, 220, "T3 - Chłodnica")
T4 = Tank(80, 370, 120, 80, "T4 - Produkt")

elements += [T1, T2, T3, T4]

# GRZAŁKA
elements.append(Heater(820, 340))

# CIĄGŁA RURA: T1 → T2 → T3
pipe = ThickPipe()

pipe.add(820, 220, 820, 180)     # z góry T1
pipe.add(820, 180, 620, 180)
pipe.add(620, 180, 620, 220)     # do T2
pipe.add(620, 220, 410, 220)

elements.append(pipe)

# WĘŻOWNICA (CIĄGŁA CZĘŚĆ RURY)
coil = CoilPipe(
    x=410, #wiecej daje w prawo
    y=220, #wiecej daje w dol
    height=160,
    loops=6
)
elements.append(coil)

# WYJŚCIE Z CHŁODNICY → T4 (jak na czerwono)
pipe_out = ThickPipe()
pipe_out.add(410, 380, 180, 380) #prawo B, dol B, prawo A, dol A

elements.append(pipe_out)

# POMPA (symbolicznie)
elements.append(Pump(300, 260))

# RYSOWANIE
for e in elements:
    e.draw(canvas)

root.mainloop()