import matplotlib.pyplot as plt
import numpy as np
from LineMath import rotMat


def makeArtist(node, pos=np.array([0, 0]), rot=0):
    # Creates an artist object from node
    nodePos = np.matmul(rotMat(rot), node.pos) + pos
    circle = plt.Circle(nodePos, node.r, fill=False)
    arrowbase = nodePos + node.r * np.array([0.5 * node.o, 0.5])
    arrowdelta = node.r * np.array([-node.o, 0])
    arrow = plt.Arrow(*arrowbase, *arrowdelta, node.r/2, color="r")

    return [circle, arrow]


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

    linePoint1 = node1.pos + node1.r * \
        np.array([np.cos(alpha+theta), np.sin(alpha+theta)])
    linePoint2 = node2.pos + node2.r * \
        np.array([np.cos(beta+theta), np.sin(beta+theta)])

    return np.array([linePoint1, linePoint2])


def plotShape(shape, ax, pos=np.array([0, 0]), rot=0):
    # Plots shape on axis
    # Plot all of the nodes:
    N = len(shape.nodes)

    for node in shape.nodes:
        nodeArtist = makeArtist(node, pos, rot)
        for artist in nodeArtist:
            ax.add_artist(artist)

    lines = np.array([[np.matmul(rotMat(rot), point) + pos for point in line] for line in shape.lines])
    for line in lines:
        ax.plot(line[:, 0], line[:, 1])
