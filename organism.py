from abc import ABC, abstractmethod
import random

from genome import Genome


class Organism(ABC):

    width_range = 700
    height_range = 700

    organism_tag = "organism"

    def __init__(self):
        self.genome = Genome(type(self))

        self.tag = str(id(self))
        # Do we want to make it so that Microbes cannot occupy the same pixel?
        # How are we going to store window size?
        self.x = random.randint(0, Organism.width_range - 1)
        self.y = random.randint(0, Organism.height_range - 1)

        hash_val = hash(str(self.genome))
        r = (hash_val & 0xFF0000) >> 16
        g = (hash_val & 0x00FF00) >> 8
        b = hash_val & 0x0000FF
        self.color = "#%02x%02x%02x" % (r, g, b)

    @abstractmethod
    def move(self):
        pass
