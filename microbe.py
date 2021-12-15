import typing

from genome import Genome


class Microbe:

    # May want to later change num_genes to be dependent on organism class
    def __init__(self, num_genes):
        self.genome = Genome(num_genes, Microbe)
        self.color = self._get_color()

    @classmethod
    def from_genome(cls, genome: Genome):
        m = Microbe(genome.num_genes)
        # bad practice to initiate the genome then rewrite?
        m.genome = genome
        m.color = m._get_color()

        return m

    # Overwrite add function to allow for breeding
    def __add__(self, other):
        # assert that genomes are of the same organism type and length
        g = self.genome + other.genome
        m = Microbe.from_genome(g)

        return m

    def _get_color(self):
        hash_val = hash(str(self.genome))
        r = (hash_val & 0xFF0000) >> 16
        g = (hash_val & 0x00FF00) >> 8
        b = hash_val & 0x0000FF
        return r, g, b

    # Returns number of: (input nodes, hidden nodes, output nodes)
    @staticmethod
    def get_brain_structure():
        return 17, 3, 8
