import numpy as np
from copy import deepcopy

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from Tester import moveSequence
from Polygon import Polygon

plt.style.use('fivethirtyeight')

xs = [0]*25 + list(np.linspace(0,-0.5,25)) + [-0.5]*25 + list(np.linspace(-0.5,0,25))
ys = list(np.linspace(0,-0.5,25)) + [-0.5]*25 + list(np.linspace(-0.5,0,25)) + [0]*25
original = Polygon(xs, ys)


# Generate original population
population = []
popSize = 10
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
        newPopulation.append(p.createOffspring())
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


# View hall of fame stuff
for p in halloffame:
    plt.figure()
    plt.fill(p.xs, p.ys)
    plt.xlim(-1,1)
    plt.ylim(-1,1)

plt.show()
