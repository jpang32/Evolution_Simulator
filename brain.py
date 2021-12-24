import math
import numpy as np
from scipy.sparse import csr_matrix
import time
from scipy.special import softmax

class Brain:

    # Keeping it simply for now:
    # [lx, ly, lastx, lasty, pop_density]
    num_input_nodes = 5
    num_hidden_nodes = 4
    # [UP, DOWN, RIGHT, LEFT, RANDOM, STILL, REVERSE]
    num_output_nodes = 6

    class Sensory:

        def __init__(self, this_brain):
            self.organism = this_brain.organism
            '''
            # Redundant for now - may be useful if we decide to place organism outside
            # of grid borders
            self.bdx = math.abs(organism.x)
            self.bdy = math.abs(organism.y)
            '''

        # World location on x axis
        def get_lx(self):
            return self.organism.x / type(self.organism).width_range

        # World location on y axis
        def get_ly(self):
            return self.organism.y / type(self.organism).height_range

        # Last move in x direction (+ for right, - for left, or None for N/A)
        def get_lastx(self):
            return self.organism.lastx

        # Last move in y direction (+ for right, - for left, or None for N/A)
        def get_lasty(self):
            return self.organism.lasty

        # Direction the organism is facing
        def get_direction(self):
            return self.organism.direction

        # Get population density within rectangle (ie, the "neighborhood")
        # Width will always be centered, but height may simply start
        def get_pop_density(self, x1=None, y1=None, x2=None, y2=None):
            if x1 is None and x2 is not None:
                raise Exception('x1 undefined')
            if y1 is None and y2 is not None:
                raise Exception('y1 undefined')

            if x2 is None:
                x2 = x1
            if y2 is None:
                y2 = y1

            if x1 is None:
                x1 = x2 = type(self.organism).range
            if y1 is None:
                y1 = y2 = type(self.organism).range

            roi_width = x2 + x1 + 1
            roi_height = y1 + y2 + 1

            num_neighbors = len(self.organism.env.find_enclosed(self.get_lx() - x1,
                                                        self.get_ly() - y1,
                                                        self.get_lx() + x2,
                                                        self.get_ly() + y2))

            # TODO: Cut the region so that it doesn't include space off of the canvas

            # Will probably give a very low number - may want to weight it differently in the future
            return num_neighbors / (roi_width * roi_height)

        # IMPORTANT: Gets sensory data in following order:
        # [lx, ly, lastx, lasty, pop_density]
        def get_data(self):
            data = [self.get_lx(),
                    self.get_ly(),
                    self.get_lastx(),
                    self.get_lasty(),
                    self.get_pop_density()]

            return data

        # Returns population densities in (forward, backward, left, right) directions
        # TODO: May need to be fixed in the future
        def get_directional_gradients(self):
            # the width of the ROI
            roi_thickness = 1 # Makes total thickness 3
            roi_length = type(self.organism).range

            # [UP, DOWN, RIGHT, LEFT]
            gradients = []

            # UP
            x1 = x2 = roi_thickness
            y1 = roi_length
            y2 = 0
            gradients.append(self.get_pop_density(x1, y1, x2, y2))

            # DOWN
            x1 = x2 = roi_thickness
            y1 = 0
            y2 = roi_length
            gradients.append(self.get_pop_density(x1, y1, x2, y2))

            # RIGHT
            y1 = y2 = roi_thickness
            x1 = 0
            x2 = roi_length
            gradients.append(self.get_pop_density(x1, y1, x2, y2))

            # LEFT
            y1 = y2 = roi_thickness
            x1 = roi_length
            x2 = 0
            gradients.append(self.get_pop_density(x1, y1, x2, y2))

            return gradients

        '''
        def bdx(self):
            math.abs(self.organism.x)

        def bdy(self):
            math.abs(self.organism.y)
        '''

    def __init__(self, organism):
        self.organism = organism
        self.sensory = self.Sensory(self)

    # Can this be sped up?
    def think(self):
        # Equation: B(Ax + d) + c = y
        # where x is input node vector
        # A[i, j] takes weight value from input node j to hidden node i
        # d[l] takes weight value from input (TODO: Ignoring this for now)
        # B[k, i] takes weight value from hidden node i to output node k
        # c[k] takes weight from input nodes to output node k

        x = np.array(self.sensory.get_data(), dtype='d').reshape(self.num_input_nodes, 1)

        #print('Inputs: ', x)

        A = self.organism.A
        B = self.organism.B
        c = self.organism.c

        y = softmax(np.matmul(B, np.tanh(np.matmul(A, x))) + c)

        assert y.shape[0] == Brain.num_output_nodes

        return y.reshape((Brain.num_output_nodes,))


