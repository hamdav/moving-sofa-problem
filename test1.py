import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Polygon import Polygon

plt.style.use('fivethirtyeight')

def isThrough(p):
    return (p.xs >= 0).all


def scooch(p, next_point):
    # Move p small amount so that the next point is at corner
    # Returns true if operation has been done and
    # false if it cannot be done
    dTheta = 0.05

    # Translate shape
    moveBy = (0-p.xs[next_point], 0-p.ys[next_point])
    p.translate(moveBy)

    # Check if some points are above y=1 and some down right
    # If so, we cannot rotate to solve the problem
    if any(np.logical_and(p.xs > 0, p.ys < 0)) and any(p.ys > 1):
        return False

    # Find all points that are out of bounds
    isOut = np.logical_or((p.xs < -1), np.logical_or((p.ys > 1), np.logical_and(p.xs > 0, p.ys < 0)))
    indeces = [i for i, b in enumerate(isOut) if b]

    # Rotate to make these in bounds again
    for index in indeces:
        if p.xs[index] < -1:
            print("shouldn't happen")

        while p.xs[index] > 0 and p.ys[index] < 0:
            p.rotate((0, 0), -dTheta)

        while p.ys[index] > 1:
            p.rotate((0, 0), dTheta)

        isOut = (p.xs < -1) or (p.ys > 1) or (p.xs > 0 and p.ys < 0)
        noNewOuts = all([i in indeces for i, b in enumerate(isOut) if b])
        if not noNewOuts:
            return False

    return True



fig = plt.figure()
ax = fig.add_subplot()

ax.hlines(0,0,3)
ax.hlines(1,-1,3)
ax.vlines(0,-3,0)
ax.vlines(-1,-3,1)


p = Polygon([0, -0.2, -0.25, -0.1, 0, -0.5, -0.5],
            [0, -0.2, -0.5, -0.6, -0.7, -0.7, 0])
ax.fill(p.xs, p.ys)


def animate(i):
    ax.clear()
    scooch(p, i)
    ax.fill(p.xs, p.ys)
    ax.hlines(0,0,3)
    ax.hlines(1,-1,3)
    ax.vlines(0,-3,0)
    ax.vlines(-1,-3,1)


anim = FuncAnimation(fig, animate, frames=4, repeat_delay = 1000)
plt.show()


