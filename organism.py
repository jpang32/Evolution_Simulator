from abc import ABC, abstractmethod
import random
from enum import Enum
import math

from genome import Genome
from brain import Brain

import numpy as np
from scipy.sparse import csr_matrix

import time


class Direction(Enum):
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3
    RANDOM = 4
    STILL = 5


class Organism(ABC):

    env = None
    width_range = None
    height_range = None

    organism_tag = "organism"

    def __init__(self):
        self.genome = Genome(type(self))

        self.brain = Brain(self)

        self.tag = str(id(self))
        # Do we want to make it so that Microbes cannot occupy the same pixel?
        # How are we going to store window size?
        self.x = random.randint(0, Organism.width_range - 1)
        self.y = random.randint(0, Organism.height_range - 1)

        self.direction = random.choice(list(Direction)).value
        self.lastx = 0
        self.lasty = 0

        self._shape = None


    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x


    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        self._shape = shape


    @property
    def genome(self):
        return self._genome

    @genome.setter
    def genome(self, g: Genome):
        self._genome = g
        self.A, self.B, self.c = self.__get_genome_matrices()
        self.color = "#%02x%02x%02x" % self.__get_color()

    def __get_color(self):
        r = 0
        g = 0
        b = 0

        for gene in self._genome.genome:
            hash_val = hash(gene)
            r += ((hash_val & 0xFF0000) >> 16)
            g += ((hash_val & 0x00FF00) >> 8)
            b += (hash_val & 0x0000FF)

        m = int('11111111', 2)
        n = len(self.genome)

        avg = m * n / 2
        std = math.sqrt(n * m * m / 12)

        r -= avg
        g -= avg
        b -= avg

        r /= std
        g /= std
        b /= std

        r = math.erf(r)
        g = math.erf(g)
        b = math.erf(b)

        r += 1
        g += 1
        b += 1

        r *= 255 / 2
        g *= 255 / 2
        b *= 255 / 2

        return int(r), int(g), int(b)

    def __get_genome_matrices(self):

        rows_A = []  # Indices of hidden nodes
        cols_A = []  # Indices of input nodes
        data_A = []  # Input to hidden weight values

        rows_B = []  # Indices of output nodes
        cols_B = []  # Indices of hidden nodes
        data_B = []  # Hidden to output weight values

        rows_c = []  # Indices of output nodes (from direct input node connections)
        cols_c = []
        data_c = []  # Input to output weight values

        for gene in self._genome.genome:

            source_type = (gene & (1 << 31)) >> 31
            source_id = (gene & (int('1111111', 2) << 24)) >> 24
            source_id %= Brain.num_hidden_nodes if source_type else Brain.num_input_nodes
            sink_type = (gene & (1 << 23)) >> 23
            sink_id = (gene & (int('1111111', 2) << 16)) >> 16
            sink_id %= Brain.num_hidden_nodes if sink_type else Brain.num_output_nodes
            weight = (gene & int('1111111111111111', 2)) - 32768
            # We want weight to be about between -4.0 and 4.0
            weight /= 8200

            assert (source_type == 0 or source_type == 1)
            assert (sink_type == 0 or sink_type == 1)
            if source_type == 1:
                assert (source_id < Brain.num_hidden_nodes)
            if source_type == 0:
                assert (source_id < Brain.num_input_nodes)
            if sink_type == 1:
                assert (sink_id < Brain.num_hidden_nodes)
            if sink_type == 0:
                assert (sink_id < Brain.num_output_nodes)
            assert (-4.0 < weight < 4.0)

            # Case where the input node goes directly to output
            if source_type == 0 and sink_type == 0:
                rows_c.append(sink_id)
                cols_c.append(0)
                data_c.append(weight)
            elif source_type == 0 and sink_type == 1:
                rows_A.append(sink_id)
                cols_A.append(source_id)
                data_A.append(weight)
            elif source_type == 1 and sink_type == 0:
                rows_B.append(sink_id)
                cols_B.append(source_id)
                data_B.append(weight)
            elif source_type == 1 and sink_type == 1:
                continue  # Ignoring interconnected hidden nodes for now

        A = csr_matrix((data_A, (rows_A, cols_A)),
                       shape=(Brain.num_hidden_nodes, Brain.num_input_nodes), dtype='f4')
        B = csr_matrix((data_B, (rows_B, cols_B)),
                       shape=(Brain.num_output_nodes, Brain.num_hidden_nodes), dtype='f4')
        c = csr_matrix((data_c, (rows_c, cols_c)),
                       shape=(Brain.num_output_nodes, 1), dtype='f4')

        return A.toarray(), B.toarray(), c.toarray()

    # Used for clamping x and y value
    @staticmethod
    def clamp(n, minn, maxn):
        return max(min(maxn, n), minn)

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def set_canvas_object(self, env):
        pass

    @abstractmethod
    def move(self, env_data):
        pass
