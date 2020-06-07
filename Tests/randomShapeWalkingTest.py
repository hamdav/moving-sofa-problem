from Shape import Node
from Shape import Shape
from PlotShape import showShape
from ShapeValidTest import getWalk, shapeIsValid
from PlotShape import animateWalk

import numpy as np
np.random.seed(4)

for i in range(10):
    print(f"Creating shape number {i}")
    s = Shape(xlim=[-0.5, 0.5], ylim=[-3.5, -0.5])
    # showShape(s)

    print(f"Walking shape number {i}")
    poss, rots = getWalk(s)
    print(f"Shape was valid: {shapeIsValid(s)}")
    print(f"Animating shape number {i}")
    animateWalk(s, poss, rots, filename=f"walk{i}")
    print("   -   ")

nodes = [Node([0, 0], 0.1, 1)]
nodes.append(Node([0, -1.1], 0.1, 1))
nodes.append(Node([0.2, -0.8], 0.1, -1))
nodes.append(Node([0.4, -0.79], 0.1, 1))

s = Shape(nodes)
poss, rots = getWalk(s)
#animateWalk(s, poss, rots)

nodes = [Node([0, 0], 0.1, 1)]
nodes.append(Node([0, -1.0], 0.1, 1))
nodes.append(Node([0.8, -1.0], 0.1, 1))
nodes.append(Node([0.8, 0], 0.1, 1))

s = Shape(nodes)
poss, rots = getWalk(s)
#animateWalk(s, poss, rots)
