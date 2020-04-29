from PlotShape import binding_line
from PlotShape import plotShape
from Shape import Node
from Shape import Shape
import matplotlib.pyplot as plt
import numpy as np


def make_artist(node):
    circle = plt.Circle(node.pos, node.r)
    arrowbase = node.pos + node.r * np.array([0.5 * node.o, 0.5])
    arrowdelta = node.r * np.array([-node.o, 0])
    arrow = plt.Arrow(*arrowbase, *arrowdelta, node.r/2, color="r")

    return [circle, arrow]


def testShapePlotting():
    nodes = [Node([0,0],1,1,0)]
    nodes.append(Node([5,1],1,-1,1))
    nodes.append(Node([4,-6],1,1,2))
    nodes.append(Node([7,3],1,1,3))
    s = Shape(nodes)

    fig, ax = plt.subplots()
    ax.set_ylim(-10, 10)
    ax.set_xlim(-10, 10)

    plotShape(s, ax)
    plt.show()

def testAreaFunction():
    #nodes = [Node([-6,0],1,-1,0)]
    #nodes.append(Node([0,-3],6,-1,1))
    #nodes.append(Node([6,0],1,-1,2))
    #nodes.append(Node([0,-3],1,-1,3))
    nodes = [Node([-5,5],1,-1,0)]
    nodes.append(Node([0,10],5,1,4))
    nodes.append(Node([5,5],1,-1,1))
    nodes.append(Node([5,-5],1,-1,2))
    nodes.append(Node([-5,-5],1,-1,3))
    s = Shape(nodes)

    print(f"The area of the shape is: {s.area}")

    fig, ax = plt.subplots()
    ax.set_ylim(-10, 10)
    ax.set_xlim(-10, 10)

    plotShape(s, ax)
    plt.show()

testAreaFunction()

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
    patches.extend(make_artist(node1))
    patches.extend(make_artist(node2))
    patches.extend(make_artist(node3))
    patches.extend(make_artist(node4))
    patches.extend(make_artist(node5))
    patches.extend(make_artist(node6))
    patches.extend(make_artist(node7))
    patches.extend(make_artist(node8))

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
