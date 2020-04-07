import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from copy import deepcopy
from Polygon import Polygon

plt.style.use('fivethirtyeight')

def isThrough(p):
    return all(p.ys >= 0)


dTheta = 0.05

def scooch(p, next_point):
    # Move p small amount so that the next point is at corner
    # Returns true if operation has been done and
    # false if it cannot be done

    # Translate shape
    moveBy = np.array([0-p.xs[next_point], 0-p.ys[next_point]])
    p.translate(moveBy)

    # Check if there are any points out of bounds,
    # If not, we're good to go
    if not (any(np.logical_and(p.xs > 0, p.ys < 0)) or any(p.ys > 1)):
        return True

    # Translate back, rotate a bit
    p.translate(-moveBy)
    p.rotate((0, 0), -dTheta)

    # Check if there are points out of bounds after rotation
    # If so, there is nothing to do
    if (any(np.logical_and(p.xs > 0, p.ys < 0)) or any(p.ys > 1)):
        p.rotate((0,0), dTheta)
        return False

    # Otherwise, try again
    return scooch(p, next_point)

def moveSequence(p, seq):
    # Returns a sequence of pxs and pys that navigates p through the corridor if posible, otherwise returns None
    # p - polygon, seq - sequence so far as [(p1.xs, p1.ys),(p2.xs ...

    # If 
    if isThrough(p):
        return seq

    tmP = deepcopy(p)
    scooch(tmP, len(seq))


fig = plt.figure()
ax = fig.add_subplot()

ax.hlines(0,0,3)
ax.hlines(1,-1,3)
ax.vlines(0,-3,0)
ax.vlines(-1,-3,1)


#xs = list(np.linspace(0,-0.25,10)) + list(np.linspace(-0.25,-0.1,10)) + [0,-0.6,-0.6]
#ys = list(np.linspace(0,-0.9,21)) + [-0.9,0]
xs = [0]*20 + [-0.5]*20
ys = list(np.linspace(0, -1.1, 20)) + list(np.linspace(-1.1, 0, 20))

#p = Polygon([0, -0.2, -0.25, -0.1, 0, -0.5, -0.5],
            #[0, -0.2, -0.5, -0.6, -0.7, -0.7, 0])
p = Polygon(xs, ys)



def animate(i):
    ax.clear()
    success = scooch(p, i)
    if success:
        col = "b"
    else:
        col = "r"

    ax.fill(p.xs, p.ys, color=col)
    ax.hlines(0,0,3)
    ax.hlines(1,-1,3)
    ax.vlines(0,-3,0)
    ax.vlines(-1,-3,1)


anim = FuncAnimation(fig, animate, init_func=init, frames=20, repeat_delay=1000)
plt.show()


