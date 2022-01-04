import numpy as np
import numba


class Brain:

    # Keeping it simple for now:
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

        # IMPORTANT: Gets sensory data in following order:
        # [lx, ly, lastx, lasty, pop_density]
        def get_data(self):
            data = [self.get_lx(),
                    self.get_ly(),
                    self.get_lastx(),
                    self.get_lasty()]

            return data

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
    def think(self, env_data):
        # Equation: B(Ax + d) + c = y
        # where x is input node vector
        # A[i, j] takes weight value from input node j to hidden node i
        # d[l] takes weight value from input (TODO: Ignoring this for now)
        # B[k, i] takes weight value from hidden node i to output node k
        # c[k] takes weight from input nodes to output node k

        sensory_data = self.sensory.get_data() + env_data
        x = np.array(sensory_data, dtype='f4').reshape(self.num_input_nodes, 1)

        A = self.organism.A
        B = self.organism.B
        c = self.organism.c

        y = Brain._think(A, B, c, x)

        return y

    @numba.jit(nopython=True)
    def _think(A, B, c, x):

        # Equation: B(Ax + d) + c = y
        # where x is input node vector
        # A[i, j] takes weight value from input node j to hidden node i
        # d[l] takes weight value from input (TODO: Ignoring this for now)
        # B[k, i] takes weight value from hidden node i to output node k
        # c[k] takes weight from input nodes to output node k

        y = B @ A @ x + c

        e_y = np.exp(y - np.max(y))

        e_y = e_y / e_y.sum(axis=0)

        return list(e_y)

