import numpy as np

from Shape import Shape
from Shape import Node


def randomNode(xlim=(-0.5, 0.5), ylim=(-0.5, 0.5), o=None):
    # Generate orientation
    if o is None:
        o = np.random.randint(1) * 2 - 1

    # Generate positions within x- and ylim
    sizes = np.array([xlim[1] - xlim[0], ylim[1] - ylim[0]])
    pos = np.random.random_sample(size=2) * sizes + [xlim[1], ylim[0]]

    # Generate radius such that constraints are upheld
    maximumR = min(np.abs([pos[0] - xlim[0], pos[0] - xlim[1],
                           pos[1] - ylim[0], pos[1] - ylim[1]]))
    r = np.random.random_sample() * maximumR

    return Node(pos, r, o)


def randomShape(xlim=(-0.5, 0.5), ylim=(-0.5, 0.5)):
    # Decide number of nodes between 3 (incl) and 10 (excl)
    noOfNodes = np.random.randint(3, 10)

    # Generate two nodes with positive orientation as a start
    nodes = [randomNode(xlim, ylim, 1), randomNode(xlim, ylim, 1)]

    # Keep track of the tries, don't make too many
    tries = 0
    # Generate nodes
    while len(nodes) < noOfNodes:
        newNode = randomNode(xlim, ylim)
        s = Shape(nodes + [newNode])
        if s.valid:
            nodes.append(newNode)

        tries += 1
        # If we've tried more than 500 times, start over
        if tries > 500:
            return randomShape(xlim, ylim)

    return Shape(nodes)
