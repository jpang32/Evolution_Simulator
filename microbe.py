from __future__ import annotations
import random

from genome import Genome
from organism import Organism
from organism import Direction


class Error(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class IncompatibleGenome(Error):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Microbe(Organism):

    microbe_tag = "microbe"
    num_genes = 10
    range = 60

    width = 3
    height = 3

    # May want to later change num_genes to be dependent on organism class
    def __init__(self):
        super().__init__()

    @classmethod
    def from_genome(cls, genome: Genome):
        if genome.num_genes != Microbe.num_genes or genome.organism_type != Microbe:
            raise IncompatibleGenome("Incompatible Genome for Microbe.")
        m = Microbe()
        # bad practice to initiate the genome then rewrite?
        m.genome = genome

        return m

    # Returns number of: (input nodes, hidden nodes, output nodes)
    @staticmethod
    def get_brain_structure():
        return 17, 3, 8

    def reset(self):
        self.x = random.randint(0, Organism.width_range - 1)
        self.y = random.randint(0, Organism.height_range - 1)

    def set_canvas_object(self, env):
        return env.create_rectangle(self.x, self.y,
                                    self.x + Microbe.width,
                                    self.y + Microbe.height,
                                    fill=self.color)

    def move(self, env_data, direction=None):

        # Must update direction
        if direction is None:
            outputs = self.brain.think(env_data)
            out = random.choices(list(Direction), weights=outputs, k=1)[0].value
        else:
            out = direction

        # Avg time for the rest of the function: 4.05e-06
        if out == Direction.UP.value:
            self.direction = out
            self.lasty = -1
            self.y -= 1
        elif out == Direction.DOWN.value:
            self.lasty = 1
            self.direction = out
            self.y += 1
        elif out == Direction.RIGHT.value:
            self.lastx += 1
            self.direction = out
            self.x += 1
        elif out == Direction.LEFT.value:
            self.lastx -= 1
            self.direction = out
            self.x -= 1
        elif out == Direction.RANDOM.value:
            self.move(env_data, direction=random.choice(list(Direction)[0:4]).value)

        self.x = Organism.clamp(self.x, 0, Organism.width_range - Microbe.width)
        self.y = Organism.clamp(self.y, 0, Organism.height_range - Microbe.height)

    # Overwrite add function to allow for breeding
    def __add__(self, other):
        # assert that genomes are of the same organism type and length
        g = self.genome + other.genome
        m = Microbe.from_genome(g)

        return m
