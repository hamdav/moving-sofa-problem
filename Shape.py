import numpy as np


class Node:
    def __init__(self, pos, radius, orientation):
        # X and Y position on center
        self.pos = np.array(pos)
        # Radius
        self.r = radius
        # Orientation (+1 or -1) denotes which way around the boundry goes
        self.o = orientation


class Shape:
    def __init__(self, nodes):
        self.nodes = nodes

    #def calculateArea(self):
