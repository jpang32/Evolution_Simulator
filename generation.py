from __future__ import annotations
from microbe import Microbe
import random


class Generation:

    def __init__(self):
        self.microbes = []

    # This needs to be fixed when we figure out how to deal with killing
    # microbes in environment
    @classmethod
    def from_generation(cls, gen: Generation):
        g = Generation()
        for i in range(len(gen.microbes)):
            j = random.randint(0, len(gen.microbes) - 1)
            k = random.randint(0, len(gen.microbes) - 1)
            g.microbes.append(gen.microbes[j] + gen.microbes[k])
        return g

    def add_members(self, size):
        for i in range(size):
            self.microbes.append(Microbe())
