import random
import typing
import tkinter as tk

from genome import Genome


class Microbe:

    #root = tk.Tk()
    win_height = 700
    win_width = 700
    #canvas = tk.Canvas(root, bg='white', height=win_height, width=win_width)
    tag = "microbe"

    # May want to later change num_genes to be dependent on organism class
    def __init__(self, num_genes):
        self.genome = Genome(num_genes, Microbe)
        self.color = self._get_color()
        self.tag = str(id(self))
        # Do we want to make it so that Microbes cannot occupy the same pixel?
        self.x = random.randint(0, Microbe.win_width - 1)
        self.y = random.randint(0, Microbe.win_height - 1)

    @classmethod
    def from_genome(cls, genome: Genome):
        m = Microbe(genome.num_genes)
        # bad practice to initiate the genome then rewrite?
        m.genome = genome
        m.color = m._get_color()

        return m

    # Returns number of: (input nodes, hidden nodes, output nodes)
    @staticmethod
    def get_brain_structure():
        return 17, 3, 8

    # Overwrite add function to allow for breeding
    def __add__(self, other):
        # assert that genomes are of the same organism type and length
        g = self.genome + other.genome
        m = Microbe.from_genome(g)

        return m

    def move(self):
        # For now, they will just move upward.
        # In the future, they will use their brain to make a decision
        if self.y > 0:
            self.y -= 1

    def _get_color(self):
        hash_val = hash(str(self.genome))
        r = (hash_val & 0xFF0000) >> 16
        g = (hash_val & 0x00FF00) >> 8
        b = hash_val & 0x0000FF

        return "#%02x%02x%02x" % (r, g, b)

