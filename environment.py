import tkinter as tk
from typing import List
from microbe import Microbe
from generation import Generation

import time


class Environment(tk.Canvas):

    duration = 10 * 1000 # Max duration in milliseconds
    clock = 0 # Current duration in milliseconds

    safe_x = [200, 400] # [x1, x2] safe area
    safe_y = [200, 400] # [y1, y2] safe area

    def __init__(self, root, height, width, generation: Generation, frame_rate):
        super().__init__(root, height=height, width=width, bg="white")
        self.generation = generation
        self.frame_rate = frame_rate
        self.width = width
        self.height = height

    def tick(self):
        # if time is up: transition (create new generation)
        if Environment.duration <= Environment.clock:
            self.transition()
            Environment.clock = 0
        for organism in self.generation.members:
            prev_x = organism.x
            prev_y = organism.y
            organism.move()
            deltx = organism.x - prev_x
            delty = organism.y - prev_y
            self.move(organism.shape, deltx, delty)
        Environment.clock += 1000 / self.frame_rate
        self.after(int(1000 / self.frame_rate), self.tick)

    # transition to next generation
    # Calculate survivors
    # Pass them to generation function (which breeds them)
    # set self.gen equal to new gen
    def transition(self):
        self.addtag_all('dead')
        self.addtag_enclosed('alive',
                             Environment.safe_x[0],
                             Environment.safe_y[0],
                             Environment.safe_x[1],
                             Environment.safe_y[1])
        self.dtag('alive', 'dead')
        self.delete('dead')
        survivors = []
        for organism in self.generation.members:
            if 'alive' in self.gettags(organism.shape):
                survivors.append(organism)
            # Resets each to random location on map
            prev_x = organism.x
            prev_y = organism.y
            organism.reset()
            self.move(organism.shape, organism.x - prev_x, organism.y - prev_y)

        self.generation = Generation.next_gen_from_members_list(survivors)


