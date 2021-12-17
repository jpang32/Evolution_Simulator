import tkinter as tk
from typing import List
from microbe import Microbe


class Environment(tk.Canvas):

    def __init__(self, root, height, width, organisms: List[Microbe], frame_rate):
        super().__init__(root, height=height, width=width, bg="white")
        self.organisms = organisms
        self.frame_rate = frame_rate

        for organism in self.organisms:
            organism.tag = self.create_rectangle(organism.x, organism.y, organism.x + 3, organism.y + 3, fill=organism.color)

    def tick(self):
        for organism in self.organisms:
            prev_x = organism.x
            prev_y = organism.y
            organism.move()
            deltx = organism.x - prev_x
            delty = organism.y - prev_y
            self.move(organism.tag, deltx, delty)
        self.after(int(1000 / self.frame_rate), self.tick)
