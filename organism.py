from abc import ABC, abstractmethod

class Organism:

    def __init__(self):
        self.genome = Genome(Microbe.num_genes, Microbe)
        self.color = self._get_color()
        self.tag = str(id(self))
        # Do we want to make it so that Microbes cannot occupy the same pixel?
        self.x = random.randint(0, Microbe.win_width - 1)
        self.y = random.randint(0, Microbe.win_height - 1)

    def _get_color(self):
        hash_val = hash(str(self.genome))
        r = (hash_val & 0xFF0000) >> 16
        g = (hash_val & 0x00FF00) >> 8
        b = hash_val & 0x0000FF

        return "#%02x%02x%02x" % (r, g, b)