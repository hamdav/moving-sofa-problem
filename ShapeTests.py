from Plot import binding_line
from Shape import Node
import matplotlib.pyplot as plt
import numpy as np


def make_artist(node):
    circle = plt.Circle(node.pos, node.r)
    arrowbase = node.pos + node.r * np.array([0.5 * node.o, 0.5])
    arrowdelta = node.r * np.array([-node.o, 0])
    arrow = plt.Arrow(*arrowbase, *arrowdelta, node.r/2, color="r")

    return [circle, arrow]


node1 = Node([5, 5], 1, 1)
node2 = Node([3, 7], 1, 1)
node3 = Node([5, -5], 1, 1)
node4 = Node([4, -7], 1, -1)
node5 = Node([-5, -5], 1, 1)
node6 = Node([-8, -7], 0.3, -1)
node7 = Node([-5, 5], 0.3, -1)
node8 = Node([-2, 7], 1.3, 1)

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
