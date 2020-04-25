import matplotlib.pyplot as plt
import numpy as np


def binding_line(node1, node2):
    # Return line kissing both nodes on appropriate sides

    # Vector from center of 1 to center of 2
    vector12 = node2.pos - node1.pos
    dist12 = np.linalg.norm(vector12)

    # Angle vector makes with pos x axis, \in [-pi, pi]
    theta = np.arctan2(vector12[1], vector12[0])

    # Calculate angles (from vector12) where the line touches
    # If orientations are the same: 
    if node1.o * node2.o == 1:
        alpha = np.arccos((node1.r - node2.r)/dist12)
        beta = alpha
    # If orientations are different:
    elif node1.o * node2.o == -1:
        alpha = np.arccos((node1.r + node2.r)/dist12)
        beta = alpha-np.pi

    # If node1s orientation is 1, flip the signs of the angles
    alpha *= -node1.o
    beta *= -node1.o

    linePoint1 = node1.pos + node1.r*np.array([np.cos(alpha+theta), np.sin(alpha+theta)])
    linePoint2 = node2.pos + node2.r*np.array([np.cos(beta+theta), np.sin(beta+theta)])

    return np.array([linePoint1, linePoint2])

