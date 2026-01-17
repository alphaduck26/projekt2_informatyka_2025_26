class VaporStream:
    def __init__(self, path):
        self.path = path
        self.amount = 0.0
        self.particles = []

    def add(self, v):
        self.amount += v
        count = int(v * 200)
        for _ in range(count):
            self.particles.append(0.0)

    def take(self):
        v = self.amount
        self.amount = 0.0
        self.particles.clear()
        return v

    def draw(self, canvas):
        new_particles = []
        for t in self.particles:
            t += 0.03
            if t < 1.0:
                x, y = self.interpolate(t)
                canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="white")
                new_particles.append(t)
        self.particles = new_particles

    def interpolate(self, t):
        total = len(self.path) - 1
        seg = int(t * total)
        seg = min(seg, total - 1)
        lt = (t * total) - seg

        x1, y1 = self.path[seg]
        x2, y2 = self.path[seg + 1]

        return x1 + (x2 - x1) * lt, y1 + (y2 - y1) * lt