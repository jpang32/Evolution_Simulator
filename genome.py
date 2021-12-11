import typing
import random

# Delete below after testing
# from microbe import Microbe


class Genome:

    # In order to build the genes properly, this must know
    # how many neurons are in the brain

    # Would probably want to get this info from the brain within the Organism:
    # This way, if we create new types of organisms with different brains,
    # we won't have to rely on final variables from the brain class

    # Then, we should use final variables from the Microbe class

    # This init creates the first gen, which has random genes
    def __init__(self, num_genes, OrganismType):

        self.genome = []
        nodes = OrganismType.get_brain_structure()

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

    #def __init__(self, genome1: str, genome2: str):

    #def __init__(self, genome1: Genome, genome2: Genome):

    def __str__(self):
        gene_strings = []

        for gene in self.genome:
            gene_strings.append(format(gene, '08x'))

        return " ".join(gene_strings)


