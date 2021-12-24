import tkinter as tk
from typing import List
from microbe import Microbe
from generation import Generation

#from numba import int32, float32    # import the types
#from numba.experimental import jitclass


import time
import numba


class Environment(tk.Canvas):

    duration = 300 # Number of ticks before next gen
    ticks = 0 # Current number of ticks

    # temp:
    timer = 0

    safe_x = [175, 351] # [x1, x2] safe area
    safe_y = [0, 351] # [y1, y2] safe area

    def __init__(self, root, height, width, generation: Generation, frame_rate):
        super().__init__(root, height=height, width=width, bg="white")
        self.safe_area = self.create_rectangle(self.safe_x[0], self.safe_y[0],
                                               self.safe_x[1], self.safe_y[1],
                                               fill='#FFE5CC', outline='white')
        self.generation = generation
        self.frame_rate = frame_rate
        self.width = width
        self.height = height

    def tick(self):
        start = time.time()
        # if time is up: transition (create new generation)
        if Environment.duration <= Environment.ticks:
            print('Generation length: ', Environment.timer)
            Environment.timer = 0
            # Takes 22 to 23 seconds for a generation to complete
            self.transition()
            Environment.ticks = 0
        self.move_organisms()
        after_time = int(1000 / self.frame_rate)
        Environment.ticks += 1
        end = time.time()
        Environment.timer += end - start
        self.after(1, self.tick)

    def move_organisms(self):
        for organism in self.generation.members:
            prev_x = organism.x
            prev_y = organism.y
            # Avg move time for all organisms in one tick: 1.45e-04
            # Assuming 300 ticks / gen: 0.0435s
            # Of 22 to 23 seconds it takes for each gen, about 21 to 22 of those are for moving all of the organisms
            organism.move()
            deltx = organism.x - prev_x
            delty = organism.y - prev_y
            # Avg move time for all organisms in one tick: 6e-06
            # Assuming 300 ticks / gen: 1.8e-03s
            self.move(organism.shape, deltx, delty)

    # transition to next generation
    # Calculate survivors
    # Pass them to generation function (which breeds them)
    # set self.gen equal to new gen
    def transition(self):
        self.addtag_all('dead')
        self.addtag_overlapping('alive',
                             Environment.safe_x[0],
                             Environment.safe_y[0],
                             Environment.safe_x[1],
                             Environment.safe_y[1])
        area = (self.safe_x[1] - self.safe_x[0]) * (self.safe_y[1] - self.safe_y[0])
        print('Survivor density: ', len(self.find_withtag('alive')) / area)
        self.dtag('alive', 'dead')
        self.dtag(self.safe_area, 'dead')
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
        self.dtag('alive', 'alive')
        self.generation = Generation.next_gen_from_members_list(survivors)


