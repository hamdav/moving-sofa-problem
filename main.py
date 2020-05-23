import numpy as np
from copy import deepcopy
import time

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation

from PlotShape import plotShape, animateWalk
from ShapeValidTest import shapeIsValid
from ShapeValidTest import getWalk
from Shape import Node, Shape

#plt.style.use('fivethirtyeight')
np.random.seed(0)

start = time.time()

# Create original shape
nodes = [Node([0.4, 0], 0.1, 1, 0)]
nodes.append(Node([-0.0, 0], 0.1, 1, 1))
nodes.append(Node([-0.0, -0.9], 0.1, 1, 2))
nodes.append(Node([0.4, -0.9], 0.1, 1, 3))
original = Shape(nodes)



# Generate original population
population = []
popSize = 50
for _ in range(popSize):
    population.append(deepcopy(original))

# For saving the best
halloffame = []

# run N generations
N = 50
for gen in range(N):
    # Repopulate
    newPopulation = []
    for s in population:
        newPopulation.append(s)
        t = s.getOffspring()
        newPopulation.append(t)

    population = newPopulation

    # Kill those that fail the test
    for i in range(len(population))[::-1]:
        if not shapeIsValid(population[i]):
            del population[i]

    # Sort according to area
    population.sort(key=lambda x: x.area,reverse=True)

    # Print first ten generations
    if gen < 10:
        print(f"Gen: {gen}, pop: {len(population)}")
        print(f"time since start: {time.time() - start}")
    # Save best if multiple of ten
    if gen % 10 == 0:
        halloffame.append(deepcopy(population[0]))
        print(f"Gen: {gen}, pop: {len(population)}")
        print(f"time since start: {time.time() - start}")

    # If there are now popSize or fewer, don't kill anyone
    if len(population) <= popSize:
        continue

    # Kill until population size is 50 or less
    del population[popSize:-1]


fig = plt.figure()
ax = fig.add_subplot()

# View hall of fame stuff
def animate(i):
    s = halloffame[i]
    ax.clear()
    plotShape(s, ax)
    ax.set_title(f"Generation {i*10}")
    ax.set_xlim(-1,3)
    ax.set_ylim(1,-3)

anim = FuncAnimation(fig, animate, frames=len(halloffame), repeat_delay=1000)

# Set up formatting for the movie files
Writer = animation.writers['imagemagick']
writer = Writer(fps=5, bitrate=1800)

anim.save('hof.gif', writer=writer)

poss, rots = getWalk(halloffame[-1])

animateWalk(halloffame[-1], poss, rots)
