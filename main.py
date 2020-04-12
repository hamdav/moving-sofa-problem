import numpy as np
from copy import deepcopy

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from Tester import moveSequence
from Polygon import Polygon

plt.style.use('fivethirtyeight')

n=3
xs = [0]*n + list(np.linspace(0,-0.5,n,endpoint=False)) + [-0.5]*n + list(np.linspace(-0.5,0,n, endpoint=False))
ys = list(np.linspace(0,-1.1,n, endpoint=False)) + [-1.1]*n + list(np.linspace(-1.1,0,n, endpoint=False)) + [0]*n
original = Polygon(xs, ys)


# Generate original population
population = []
popSize = 50
for _ in range(popSize):
    population.append(deepcopy(original))

# For saving the best
halloffame = []

# run N generations
N = 500
for gen in range(N):
    # Repopulate
    newPopulation = []
    for p in population:
        newPopulation.append(p)
        q = p.createOffspring()
        # If the new offspring has points out of bounds, don't add it
        if (any(np.logical_and(q.xs > 0, q.ys < 0)) or any(q.ys > 1) or any(q.xs < -1)):
            continue
        else:
            newPopulation.append(q)

    population = newPopulation

    # Kill those that fail the test
    for i in range(len(population))[::-1]:
        if moveSequence(population[i]) is None:
            del population[i]

    # Sort according to area
    population.sort(key=lambda x: x.area,reverse=True)

    # Save best if multiple of ten
    if gen % 10 == 0:
        halloffame.append(deepcopy(population[0]))
        print(f"Gen: {gen}, pop: {len(population)}")

    # If there are now popSize or fewer, don't kill anyone
    if len(population) <= popSize:
        continue

    # Kill until population size is 50 or less
    del population[popSize:-1]


fig = plt.figure()
ax = fig.add_subplot()

# View hall of fame stuff
def animate(i):
    p = halloffame[i]
    ax.clear()
    ax.fill(p.xs, p.ys)
    ax.set_title(f"Generation {i*10}")
    ax.hlines(0,0,3)
    ax.hlines(1,-1,3)
    ax.vlines(0,-3,0)
    ax.vlines(-1,-3,1)

anim = FuncAnimation(fig, animate, frames=len(halloffame), repeat_delay=1000)

seq = moveSequence(halloffame[-1], [], 0)

fig2 = plt.figure()
ax2 = fig2.add_subplot()

def animate2(i):
    ax2.clear()
    ax2.fill(seq[i][0], seq[i][1])
    ax2.hlines(0,0,3)
    ax2.hlines(1,-1,3)
    ax2.vlines(0,-3,0)
    ax2.vlines(-1,-3,1)


anim2 = FuncAnimation(fig2, animate2, frames=len(seq), repeat_delay=1000)
plt.show()
