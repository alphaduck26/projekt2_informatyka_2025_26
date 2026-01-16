class ProcessScreen:
    def __init__(self):
        self.elements = []

    def add(self, element):
        self.elements.append(element)

    def draw(self, canvas):
        for e in self.elements:
            e.draw(canvas)
