import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
from matplotlib import patches
import numpy as np

from LineMath import rotMat
from ShapeValidTest import isInBounds


def makeArtist(node, nodeAngles, pos=np.array([0, 0]), rot=0):
    "Creates an artist object from node"

    if node.o == -1:
        nodeAngles = nodeAngles[::-1]

    # Calculate position
    nodePos = np.matmul(rotMat(rot), node.pos) + pos
    # Calculate angles (in degrees)
    nodeAngles = [((nodeAngles[0] + rot) % (2 * np.pi)) * 180 / np.pi,
                  ((nodeAngles[1] + rot) % (2 * np.pi)) * 180 / np.pi]
    # Create arcs
    arcIn = patches.Arc(nodePos, 2*node.r, 2*node.r, 0, *nodeAngles, color='k')
    arcOut = patches.Arc(nodePos, 2*node.r, 2*node.r, 0, *nodeAngles[::-1],
                         linestyle='--', color='gainsboro')
    # Create arrow
    arrowbase = nodePos + node.r * np.array([0.5 * node.o, 0.5])
    arrowdelta = node.r * np.array([-node.o, 0])
    arrow = plt.Arrow(*arrowbase, *arrowdelta, node.r/2, color="mistyrose")

    return [arcIn, arcOut, arrow]


def binding_line(node1, node2):
    "Return line kissing both nodes on appropriate sides"

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
    "Plots shape on axis"

    # Plot all of the nodes:
    for node in shape.nodes:
        nodeArtists = makeArtist(node, shape.nodeAngles[node.ID], pos, rot)
        for artist in nodeArtists:
            ax.add_artist(artist)

    # Plot the lines
    lines = np.array([[np.matmul(rotMat(rot), point) +
                       pos for point in line] for line in shape.lines])
    for line in lines:
        ax.plot(line[:, 0], line[:, 1])


def showShape(shape, pos=np.array([0, 0]), rot=0):
    "Shows fig of shape"

    fig, ax = plt.subplots()

    plotShape(shape, ax, pos, rot)
    ax.set_ylim(-4, 1)
    ax.set_xlim(-1, 2)
    ax.plot([0.5, 0.5, 2], [-4, -0.5, -0.5], 'k')
    ax.plot([-0.5, -0.5, 2], [-4, 0.5, 0.5], 'k')
    ax.set_title(f"inBounds: {isInBounds(shape, pos, rot)}")

    plt.show()

def saveShape(shape, pos=np.array([0, 0]), rot=0):
    "Saves fig of shape"

    fig, ax = plt.subplots()

    plotShape(shape, ax, pos, rot)
    ax.set_ylim(-2, 2)
    ax.set_xlim(-2, 2)
    ax.plot([0.5, 0.5, 2], [-2, -0.5, -0.5], 'k')
    ax.plot([-0.5, -0.5, 2], [-2, 0.5, 0.5], 'k')
    ax.set_title(f"inBounds: {isInBounds(shape, pos, rot)}")

    plt.show()


def animateWalk(shape, poss, rots):
    "Saves an animation of the walk specified by poss and rots"

    # Create figure and axis
    fig, ax = plt.subplots()

    def animate(i):
        ax.clear()
        plotShape(shape, ax, poss[i], rots[i])
        ax.set_ylim(-2, 2)
        ax.set_xlim(-2, 2)
        ax.plot([0.5, 0.5, 2], [-2, -0.5, -0.5], 'k')
        ax.plot([-0.5, -0.5, 2], [-2, 0.5, 0.5], 'k')
        ax.set_title(f"i: {i}, inBounds: {isInBounds(shape, poss[i], rots[i])}")

    anim = FuncAnimation(fig, animate, init_func=None, frames=len(
        poss), interval=10, blit=False, repeat=True, repeat_delay=0)
    # Set up formatting for the movie files
    Writer = animation.writers['imagemagick']
    writer = Writer(fps=15, bitrate=1800)

    anim.save('walk.gif', writer=writer)
