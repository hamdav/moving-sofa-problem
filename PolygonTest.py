import numpy as np
import matplotlib.pyplot as plt

from Polygon import Polygon

p = Polygon([0, 0.5, 1, 1, 0.5, 0],  [0, 0, 0, 1, 1, 1])

fig = plt.figure()
ax = fig.add_subplot()

ax.fill(p.xs, p.ys)

p.rotate((1, 0), 0.5)
ax.fill(p.xs, p.ys)

p.translate([1, 2])
ax.fill(p.xs, p.ys)


plt.show()
