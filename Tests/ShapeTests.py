import matplotlib.pyplot as plt
import numpy as np

from PlotShape import binding_line
from PlotShape import plotShape
from Shape import Node
from Shape import Shape
from ShapeValidTest import isInBounds
from PlotShape import makeArtist
from PlotShape import animateWalk
from ShapeValidTest import shapeIsValid


def testShapePlotting():
    nodes = [Node([0, 0], 1, 1, 0)]
    nodes.append(Node([5, 1], 1, -1, 1))
    nodes.append(Node([4, -6], 1, 1, 2))
    nodes.append(Node([7, 3], 1, 1, 3))
    s = Shape(nodes)

    fig, ax = plt.subplots()
    ax.set_ylim(-10, 10)
    ax.set_xlim(-10, 10)
    plotShape(s, ax, [-5, -5], 0)

    fig, ax = plt.subplots()
    ax.set_ylim(-10, 10)
    ax.set_xlim(-10, 10)
    plotShape(s, ax, [-5, -5], 0.5)

    fig, ax = plt.subplots()
    ax.set_ylim(-10, 10)
    ax.set_xlim(-10, 10)
    plotShape(s, ax, [-5, -5], 1.0)

    fig, ax = plt.subplots()
    ax.set_ylim(-10, 10)
    ax.set_xlim(-10, 10)
    plotShape(s, ax, [-5, -5], 1.5)

    fig, ax = plt.subplots()
    ax.set_ylim(-10, 10)
    ax.set_xlim(-10, 10)
    plotShape(s, ax, [-4, -4], 1.5)

    fig, ax = plt.subplots()
    ax.set_ylim(-10, 10)
    ax.set_xlim(-10, 10)
    plotShape(s, ax, [-3, -3], 1.5)

    plt.show()


def testShapeOrientation():
    nodes = [Node([0, 0], 1, 1, 0)]
    nodes.append(Node([5, 1], 1, -1, 1))
    nodes.append(Node([4, -6], 1, 1, 2))
    nodes.append(Node([7, 3], 1, 1, 3))
    s1 = Shape(nodes)

    fig, ax = plt.subplots()
    ax.set_ylim(-10, 10)
    ax.set_xlim(-10, 10)

    plotShape(s1, ax)
    ax.set_title(f"Shape orientation is {s1.o}")

    nodes2 = [Node([0, 0], 1, -1, 0)]
    nodes2.append(Node([7, 3], 1, -1, 3))
    nodes2.append(Node([4, -6], 1, -1, 2))
    nodes2.append(Node([5, 1], 1, 1, 1))
    s2 = Shape(nodes2)

    fig2, ax2 = plt.subplots()
    ax2.set_ylim(-10, 10)
    ax2.set_xlim(-10, 10)

    plotShape(s2, ax2)
    ax2.set_title(f"Shape orientation is {s2.o}")

    plt.show()


def testAreaFunction():
    #nodes = [Node([-6,0],1,-1,0)]
    # nodes.append(Node([0,-3],6,-1,1))
    # nodes.append(Node([6,0],1,-1,2))
    # nodes.append(Node([0,-3],1,-1,3))
    nodes = [Node([-5, 5], 1, -1, 0)]
    nodes.append(Node([0, 10], 5, 1, 4))
    nodes.append(Node([5, 5], 1, -1, 1))
    nodes.append(Node([5, -5], 1, -1, 2))
    nodes.append(Node([-5, -5], 1, -1, 3))
    s = Shape(nodes)

    print(f"The area of the shape is: {s.area}")

    fig, ax = plt.subplots()
    ax.set_ylim(-10, 10)
    ax.set_xlim(-10, 10)

    plotShape(s, ax)
    plt.show()


def testNodesAndBindingLine():
    node1 = Node([5, 5], 1, 1, 1)
    node2 = Node([3, 7], 1, 1, 2)
    node3 = Node([5, -5], 1, 1, 3)
    node4 = Node([4, -7], 1, -1, 4)
    node5 = Node([-5, -5], 1, 1, 5)
    node6 = Node([-8, -7], 0.3, -1, 6)
    node7 = Node([-5, 5], 0.3, -1, 7)
    node8 = Node([-2, 7], 1.3, 1, 8)

    line1 = binding_line(node1, node2)
    line2 = binding_line(node3, node4)
    line3 = binding_line(node5, node6)
    line4 = binding_line(node7, node8)

    patches = []
    patches.extend(makeArtist(node1))
    patches.extend(makeArtist(node2))
    patches.extend(makeArtist(node3))
    patches.extend(makeArtist(node4))
    patches.extend(makeArtist(node5))
    patches.extend(makeArtist(node6))
    patches.extend(makeArtist(node7))
    patches.extend(makeArtist(node8))

    fig, ax = plt.subplots()
    ax.set_ylim(-10, 10)
    ax.set_xlim(-10, 10)
# ax.grid(True)

    for patch in patches:
        ax.add_artist(patch)

    ax.plot(line1[:, 0], line1[:, 1])
    ax.plot(line2[:, 0], line2[:, 1])
    ax.plot(line3[:, 0], line3[:, 1])
    ax.plot(line4[:, 0], line4[:, 1])

    plt.show()


def testInBounds():
    nodes = [Node([0, 0], 0.1, -1, 1)]
    nodes.append(Node([0.7, 0], 0.1, -1, 2))
    nodes.append(Node([0.7, -0.3], 0.1, -1, 3))
    nodes.append(Node([0.8, -0.8], 0.3, 1, 4))
    nodes.append(Node([0.7, -1.3], 0.1, -1, 5))
    nodes.append(Node([0, -1.3], 0.1, -1, 6))
    s = Shape(nodes)

    fig, ax = plt.subplots()
    ax.set_ylim(-2, 2)
    ax.set_xlim(-2, 2)
    ax.plot([0.5, 0.5, 2], [-2, -0.5, -0.5], 'k')
    ax.plot([-0.5, -0.5, 2], [-2, 0.5, 0.5], 'k')

    pos = np.array([0.1, 0.4])
    rot = -0.3
    plotShape(s, ax, pos, rot)
    ax.set_title(f"Shape is in bounds: {isInBounds(s, pos, rot)}")
    # TODO make touching lines not intersect according to the function
    plt.show()

def testWalkAnimation():
    nodes = [Node([0.4, 0], 0.1, 1, 0)]
    nodes.append(Node([-0.3, 0], 0.1, 1, 1))
    nodes.append(Node([-0.3, -0.5], 0.1, 1, 2))
    nodes.append(Node([0.4, -0.5], 0.1, 1, 3))
    s = Shape(nodes)

    ys = np.linspace(0,1,1000)
    xs = np.zeros(1000)
    poss = np.column_stack((xs, ys))
    rots = np.linspace(0, 0.5, 1000)

    animateWalk(s, poss, rots)

