from __future__ import annotations
import random
import typing
import tkinter as tk

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

    tag = "microbe"
    num_genes = 4
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

        # Is there a more convenient way to do this?
        hash_val = hash(str(genome))
        r = (hash_val & 0xFF0000) >> 16
        g = (hash_val & 0x00FF00) >> 8
        b = hash_val & 0x0000FF
        m.color = "#%02x%02x%02x" % (r, g, b)

        return m

    # Returns number of: (input nodes, hidden nodes, output nodes)
    @staticmethod
    def get_brain_structure():
        return 17, 3, 8

    def move(self):
        # For now, they will just move upward.
        # In the future, they will use their brain to make a decision

        # Must update direction
        if self.y > 0:
            self.y -= 1
            self.direction = Direction.UP
            self.lasty = -1

    # Overwrite add function to allow for breeding
    def __add__(self, other):
        # assert that genomes are of the same organism type and length
        g = self.genome + other.genome
        m = Microbe.from_genome(g)

        return m
