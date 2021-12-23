from abc import ABC, abstractmethod
import random
from enum import Enum

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


class Organism(ABC):

    env = None

    width_range = 700
    height_range = 700

    organism_tag = "organism"

    def __init__(self):
        self.genome = Genome(type(self))
        # Used for brain thinking calculations
        self.A, self.B, self.c = self.__get_genome_matrices()
        # Hash genome to a color:
        hash_val = hash(str(self.genome))
        r = (hash_val & 0xFF0000) >> 16
        g = (hash_val & 0x00FF00) >> 8
        b = hash_val & 0x0000FF
        self.color = "#%02x%02x%02x" % (r, g, b)

        self.brain = Brain(self)

        self.tag = str(id(self))
        # Do we want to make it so that Microbes cannot occupy the same pixel?
        # How are we going to store window size?
        self.x = random.randint(0, Organism.width_range - 1)
        self.y = random.randint(0, Organism.height_range - 1)

        self.direction = random.choice(list(Direction)).value
        self.lastx = 0
        self.lasty = 0

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

        for gene in self.genome.genome:

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
                       shape=(Brain.num_hidden_nodes, Brain.num_input_nodes))
        B = csr_matrix((data_B, (rows_B, cols_B)),
                       shape=(Brain.num_output_nodes, Brain.num_hidden_nodes))
        c = csr_matrix((data_c, (rows_c, cols_c)),
                       shape=(Brain.num_output_nodes, 1))

        return A.toarray(), B.toarray(), c.toarray()

    # Used for clamping x and y value (Might need to move to Organism class in future)
    def reset(self):
        self.x = random.randint(0, Organism.width_range - 1)
        self.y = random.randint(0, Organism.height_range - 1)

    @staticmethod
    def clamp(n, minn, maxn):
        return max(min(maxn, n), minn)

    @abstractmethod
    def set_canvas_object(self):
        pass

    @abstractmethod
    def move(self):
        pass
