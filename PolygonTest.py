import numpy as np
import matplotlib.pyplot as plt

from Polygon import Polygon

xs = [0]*25 + list(np.linspace(0,-0.5,25)) + [-0.5]*25 + list(np.linspace(-0.5,0,25))
ys = list(np.linspace(0,-0.5,25)) + [-0.5]*25 + list(np.linspace(-0.5,0,25)) + [0]*25
p = Polygon(xs, ys)

fig = plt.figure()
ax = fig.add_subplot()

#ax.fill(p.xs, p.ys)

p.rotate((1, 0), 0.5)
#ax.fill(p.xs, p.ys)

p.translate([1, 2])
#ax.fill(p.xs, p.ys)

plt.ion()
for i in range(100):

    p = p.createOffspring()

    ax.clear()
    ax.fill(p.xs, p.ys)
    plt.show()
    plt.waitforbuttonpress()



