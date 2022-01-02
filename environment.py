from __future__ import annotations
import tkinter as tk
from typing import List
from organism import Organism
# from generation import Generation
import random


import time


class Environment(tk.Canvas):

    class Generation:

        count = 0
        size = 500

        def __init__(self, env):
            self.env = env
            self.members = []

        # This needs to be fixed when we figure out how to deal with killing
        # microbes in environment
        @classmethod
        def next_gen_from_members_list(cls, members, env):
            g = cls(env)
            g.members = members

            while len(g) < cls.size:
                j = random.randint(0, len(members) - 1)
                k = random.randint(0, len(members) - 1)
                new_member = members[j] + members[k]
                new_member.shape = new_member.set_canvas_object(env)
                g.members.append(new_member)

            cls.count += 1
            print('Generation ', cls.count)

            return g

        def add_members(self, members):
            for organism in members:
                organism.shape = organism.set_canvas_object(self.env)
            self.members = members

        def __len__(self):
            return len(self.members)

        # TODO: Create Iterator?

    duration = 300  # Number of ticks before next gen
    ticks = 0  # Current number of ticks

    # temp:
    timer = 0

    safe_x = [200, 401]  # [x1, x2] safe area
    safe_y = [0, 401]  # [y1, y2] safe area

    def __init__(self, root, height, width, frame_rate, num_members=500):
        super().__init__(root, height=height, width=width, bg="white")
        Organism.width_range = width
        Organism.height_range = height
        self.safe_area = self.create_rectangle(self.safe_x[0], self.safe_y[0],
                                               self.safe_x[1], self.safe_y[1],
                                               fill='#FFE5CC', outline='white')
        self.generation = self.Generation(self)
        self.frame_rate = frame_rate
        self.width = width
        self.height = height

    def add_members(self, members):
        self.generation.add_members(members)

    """BELOW: Environment sensory functions for giving info to Organisms"""

    # Get population density within rectangle (ie, the "neighborhood")
    # Width will always be centered, but height may simply start at the y value of the Organism
    def get_pop_density(self, org_x, org_y, org_range, x1=None, y1=None, x2=None, y2=None):
        if x1 is None and x2 is not None:
            raise Exception('x1 undefined')
        if y1 is None and y2 is not None:
            raise Exception('y1 undefined')

        if x2 is None:
            x2 = x1
        if y2 is None:
            y2 = y1

        if x1 is None:
            x1 = x2 = org_range
        if y1 is None:
            y1 = y2 = org_range

        roi_width = x2 + x1 + 1
        roi_height = y1 + y2 + 1

        num_neighbors = len(self.find_enclosed(org_x - x1,
                                               org_y - y1,
                                               org_x + x2,
                                               org_y + y2))

        # TODO: Cut the region so that it doesn't include space off of the canvas

        # Will probably give a very low number - may want to weight it differently in the future
        return num_neighbors / (roi_width * roi_height)

    # Returns population densities in (forward, backward, left, right) directions
    # TODO: May need to be fixed in the future
    def get_directional_gradients(self, org_x, org_y, org_range):
        # the width of the ROI
        roi_thickness = 1  # Makes total thickness 3
        roi_length = org_range

        # [UP, DOWN, RIGHT, LEFT]
        gradients = []

        # UP
        x1 = x2 = roi_thickness
        y1 = roi_length
        y2 = 0
        gradients.append(self.get_pop_density(org_x, org_y, org_range, x1, y1, x2, y2))

        # DOWN
        x1 = x2 = roi_thickness
        y1 = 0
        y2 = roi_length
        gradients.append(self.get_pop_density(org_x, org_y, org_range, x1, y1, x2, y2))

        # RIGHT
        y1 = y2 = roi_thickness
        x1 = 0
        x2 = roi_length
        gradients.append(self.get_pop_density(org_x, org_y, org_range, x1, y1, x2, y2))

        # LEFT
        y1 = y2 = roi_thickness
        x1 = roi_length
        x2 = 0
        gradients.append(self.get_pop_density(org_x, org_y, org_range, x1, y1, x2, y2))

        return gradients

    """ABOVE: Environment sensory functions for giving info to Organisms"""

    def tick(self):
        start = time.time()
        # if time is up: transition (create new generation)
        if Environment.duration <= Environment.ticks:
            print('Generation length: ', Environment.timer)
            Environment.timer = 0
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
            # Calculate env data for the organism to think
            pop_density = self.get_pop_density(organism.x, organism.y, type(organism).range)
            env_data = [pop_density]

            prev_x = organism.x
            prev_y = organism.y
            organism.move(env_data)
            deltx = organism.x - prev_x
            delty = organism.y - prev_y
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
        self.generation = self.Generation.next_gen_from_members_list(survivors, self)


