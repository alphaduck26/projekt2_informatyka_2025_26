import tkinter as tk
from tank import Tank
from heater import Heater
from pipe import ThickPipe
from coil import CoilPipe
from pump import Pump
from vapor import VaporStream

root = tk.Tk()
root.title("SCADA – Destylator")
root.resizable(False, False)

canvas = tk.Canvas(root, width=1000, height=500, bg="#A5B272")
canvas.pack(side=tk.LEFT)

ui = tk.Frame(root)
ui.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

elements = []

# ===== ZBIORNIKI =====
T1 = Tank(760,220,120,100,"T1 - Braga","#5F9EA0")
T2 = Tank(560,200,120,60,"T2 - Filtr","#8fd3ff",0.4,True)
T3 = Tank(330,200,120,220,"T3 - Chłodnica","#8fd3ff",0.8,False,True)
T4 = Tank(80,370,120,80,"T4 - Produkt","#7FFFD4")

elements += [T1, T2, T3, T4]

# ===== PIEC =====
heater = Heater(820,340)
elements.append(heater)

# ===== RURY PROCESOWE =====
pipe1 = ThickPipe()
pipe1.add_point(820,220); pipe1.add_point(820,180)
pipe1.add_point(620,180); pipe1.add_point(620,200)

pipe2 = ThickPipe()
pipe2.add_point(560,230); pipe2.add_point(410,230)

coil = CoilPipe(410,230,160)

pipe3 = ThickPipe()
pipe3.add_point(410,390); pipe3.add_point(180,390)

# ===== RURY WODNE =====
cold = ThickPipe(4,"#8fd3ff")
cold.add_point(330,240); cold.add_point(290,240)

hot = ThickPipe(4,"#ffb347")
hot.add_point(330,360); hot.add_point(290,360)

elements += [pipe1, pipe2, coil, pipe3, cold, hot, Pump(300,300)]

# ===== PARA =====
v1 = VaporStream(pipe1.points)
v2 = VaporStream(pipe2.points)
v3 = VaporStream(coil.pipe.points)
v4 = VaporStream(pipe3.points)

# ===== STATUSY =====
filter_status = tk.StringVar(value="Filtr: OK")
cooler_status = tk.StringVar(value="Chłodnica: OK")

def redraw():
    canvas.delete("all")
    for e in elements:
        e.draw(canvas)
    for v in (v1, v2, v3, v4):
        v.draw(canvas)

def process():
    # ===== ZATRZYMANIE PROCESU PODCZAS WYMIANY WODY =====
    if T2.flushing or T3.flushing:
        T2.update_flush()
        T3.update_flush()
        redraw()
        root.after(100, process)
        return

    heater.update()

    # ===== PAROWANIE =====
    if T1.level > 0 and heater.current_temp > 60:
        rate = (heater.current_temp - 60) / 30 * 0.002
        T1.remove_volume(rate)
        v1.add(rate * 5)

    # ===== FILTR =====
    passed = T2.filter(v1.take())
    if T2.filter_dirty >= 1:
        filter_status.set("UWAGA: Filtr zatkany!")
    else:
        filter_status.set("Filtr: OK")
    v2.add(passed)

    # ===== DO CHŁODNICY =====
    v3.add(v2.take())

    # ===== KONDENSACJA =====
    condensed = T3.condense(v3.take())
    if T3.temperature >= T3.max_temp:
        cooler_status.set("UWAGA: Chłodnica przegrzana!")
    else:
        cooler_status.set("Chłodnica: OK")

    v4.add(condensed * 4)
    T4.add_volume(v4.take() / 4)

    # ===== AKTUALIZACJA ANIMACJI (na wszelki wypadek) =====
    T2.update_flush()
    T3.update_flush()

    redraw()
    root.after(100, process)

# ===== UI =====
tk.Label(ui, text="Zbiornik T1 – Braga", font=("Arial",10,"bold")).pack(pady=3)
tk.Label(ui, text="Napełnianie bragi").pack()
tk.Button(ui, text="Uzupełnij",
          command=lambda: T1.fill_to(canvas, redraw, 0.9, 6000)).pack(fill="x")
tk.Label(ui, text="Opróżnianie zbiornika").pack()
tk.Button(ui, text="Opróżnij",
          command=lambda: T1.empty(canvas, redraw)).pack(fill="x")

tk.Label(ui, text="Piec", font=("Arial",10,"bold")).pack(pady=6)
tk.Label(ui, text="Włącz / wyłącz grzanie").pack()
tk.Button(ui, text="ON / OFF", command=heater.toggle).pack(fill="x")

tk.Label(ui, text="Temperatura pieca").pack()
tk.Scale(ui, from_=50, to=90, orient="horizontal",
         command=lambda v: heater.set_target(int(v))).pack(fill="x")

tk.Label(ui, textvariable=filter_status, fg="red").pack(pady=6)
tk.Label(ui, text="Wymiana filtra").pack()
tk.Button(ui, text="Wymień filtr",
          command=T2.reset_filter).pack(fill="x")

tk.Label(ui, textvariable=cooler_status, fg="red").pack(pady=6)
tk.Label(ui, text="Chłodzenie wody w chłodnicy").pack()
tk.Button(ui, text="Pompa wody",
          command=T3.cool_down).pack(fill="x")

process()
root.mainloop()
