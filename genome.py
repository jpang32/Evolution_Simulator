from __future__ import annotations
from typing import Type, TypeVar
import random

# Delete below after testing
# from microbe import Microbe


class Error(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class IncompatibleOrganisms(Error):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class IncompatibleGenomeLengths(Error):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Genome:

    # probability that one bit of a gene will be changed
    mutation_prob = 0.001

    # number of ints in a gene (may change)
    gene_bits = 32

    # In order to build the genes properly, this must know
    # how many neurons are in the brain

    # Would probably want to get this info from the brain within the Organism:
    # This way, if we create new types of organisms with different brains,
    # we won't have to rely on final variables from the brain class

    # Then, we should use final variables from the Microbe class

    # This init creates the first generation, which has random genes
    def __init__(self, num_genes: int, organism_type):

        self.genome = []
        self.num_genes = num_genes
        self.organism_type = organism_type
        nodes = organism_type.get_brain_structure()

        for i in range(num_genes):
            # 1: source type (0 for input, 1 for hidden)
            source_type = random.randint(0, 1)
            bit1 = source_type << 31
            # 2 -> 8: ID of source neuron
            bit28 = random.randint(0, 127) % (nodes[1] if source_type else nodes[0]) << 24
            # 9: sink type (1 for hidden, 0 for output)
            sink_type = random.randint(0, 1)
            bit9 = sink_type << 23
            # 10 -> 16: ID of sink neuron
            bit1016 = random.randint(0, 127) % (nodes[1] if sink_type else nodes[2]) << 16
            # 17 -> 32: weight value (divided by a number between 8000 and 10000 for 'normalization')
            bit1732 = random.randint(0, 65535)

            # gene value:
            gene = bit1 + bit28 + bit9 + bit1016 + bit1732

            self.genome.append(gene)

    # 50/50 chance of passing on a gene from each parent
    # Parameters are two Genome objects
    @classmethod
    def from_genomes(cls, genome1: Genome, genome2: Genome):

        if type(genome1) != type(genome2):
            raise IncompatibleOrganisms('Genomes not of the same organism.')
        if genome1.num_genes != genome2.num_genes:
            raise IncompatibleGenomeLengths('Genomes not of the same length.')

        new_genome = cls(genome1.num_genes, genome1.organism_type)

        new_genome.num_genes = genome1.num_genes
        new_genome.organism_type = genome1.organism_type

        #assert() that they are same length and type
        for i in range(len(genome1.genome)):
            gene = random.choice([genome1.genome[i], genome2.genome[i]])
            if random.random() < cls.mutation_prob:
                gene ^= 1 << random.randint(0, cls.gene_bits - 1)
            new_genome.genome[i] = gene

        return new_genome

    def __add__(self, other):

        return Genome.from_genomes(self, other)

    def __str__(self):
        gene_strings = []

        for gene in self.genome:
            gene_strings.append(format(gene, '08x'))

        return " ".join(gene_strings)


