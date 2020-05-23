import numpy as np
from copy import deepcopy

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from PlotShape import plotShape
from ShapeValidTest import shapeIsValid
from Shape import Node, Shape

plt.style.use('fivethirtyeight')

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
    print(f"gen:{gen}")
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
    print("HI")

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
    s = halloffame[i]
    ax.clear()
    plotShape(s, ax)
    ax.set_title(f"Generation {i*10}")

anim = FuncAnimation(fig, animate, frames=len(halloffame), repeat_delay=1000)

#seq = moveSequence(halloffame[-1], [], 0)

#fig2 = plt.figure()
#ax2 = fig2.add_subplot()

#def animate2(i):
    #ax2.clear()
    #ax2.fill(seq[i][0], seq[i][1])
    #ax2.hlines(0,0,3)
    #ax2.hlines(1,-1,3)
    #ax2.vlines(0,-3,0)
    #ax2.vlines(-1,-3,1)


#anim2 = FuncAnimation(fig2, animate2, frames=len(seq), repeat_delay=1000)
plt.show()
