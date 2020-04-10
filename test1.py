import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from Tester import moveSequence
from Polygon import Polygon

plt.style.use('fivethirtyeight')


fig = plt.figure()
ax = fig.add_subplot()

ax.hlines(0,0,3)
ax.hlines(1,-1,3)
ax.vlines(0,-3,0)
ax.vlines(-1,-3,1)


# xs = list(np.linspace(0,-0.25,10)) + list(np.linspace(-0.25,-0.1,10)) + [0,-0.6,-0.6]
# ys = list(np.linspace(0,-0.9,21)) + [-0.9,0]
# xs = [0]*20 + [-0.5]*20
# ys = list(np.linspace(0, -1.1, 20)) + list(np.linspace(-1.1, 0, 20))
xs = list(np.linspace(0,-0.5,10)) + list(np.linspace(-0.5, 0, 10)) + [-0.6,-0.6]
ys = list(np.linspace(0,-1.0,20)) + [-1.0, 0.2]

#p = Polygon([0, -0.2, -0.25, -0.1, 0, -0.5, -0.5],
            #[0, -0.2, -0.5, -0.6, -0.7, -0.7, 0])
p = Polygon(xs, ys)

seq = moveSequence(p, [], 0)


def animate(i):
    ax.clear()
    ax.fill(seq[i][0], seq[i][1])
    ax.hlines(0,0,3)
    ax.hlines(1,-1,3)
    ax.vlines(0,-3,0)
    ax.vlines(-1,-3,1)


anim = FuncAnimation(fig, animate, frames=len(seq), repeat_delay=1000)

plt.show()
