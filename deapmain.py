from deap import base
from deap import creator
from deap import tools

import time
import numpy as np
import matplotlib.pyplot as plt
import pickle

import colorama

from Shape import Shape
from ShapeValidTest import shapeIsValid, getWalk
from PlotShape import animateWalk, showShape

# Start the time
timeStart = time.time()
# Initialize colorama
colorama.init()
# Matplotlib plots pretty
plt.style.use('seaborn-darkgrid')

# The creator class creates classes.
# Use this to create the individual and population class.
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", Shape, fitness=creator.FitnessMax)

# The toolbox will hold all the objects we will use,
# like the individual, the population, as well as all functions,
# operators and arguments.
toolbox = base.Toolbox()
# Structure initializers
toolbox.register('individual', creator.Individual,
                 xlim=[-0.5, 0.5], ylim=[-3.5, -0.5])
toolbox.register('population', tools.initRepeat, list, toolbox.individual)
# Registration of tools to the toolbox associates aliases to the functions
# and freezing some of their arguments.


# Define the evaluation function
def evalOneMax(individual):
    if not individual.valid:
        return 0,
    elif not shapeIsValid(individual):
        return 0,
    else:
        return individual.area,


# Let's define som genetic operators
toolbox.register('evaluate', evalOneMax)
toolbox.register('mate', Shape.mate)
toolbox.register('mutate', Shape.mutateInPlace)
toolbox.register('select', tools.selTournament, tournsize=2)


# Now we write the main program
def main(maxGen, filename=None):
    # - - - Initial setup - - -

    # Create the population
    print(f"Creating population ({time.time() - timeStart:.0f} seconds in)")
    if filename is None:
        pop = toolbox.population(n=300)
        stats = []
    else:
        with open(filename, 'rb') as popFile:
            pop = pickle.load(popFile)
            stats = pickle.load(popFile)

    # Evaluate the entire population
    print(f"Evaluating fitnesses ({time.time() - timeStart:.0f} seconds in)")
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # Probability of mating and mutation
    MatePB, MutatePB = 0.2, 1.0

    # Extract all of the fitnesses
    fits = [ind.fitness.values[0] for ind in pop]

    # - - - Evolution - - -

    # Variable keeping track of the generations
    g = 0

    while g < maxGen:
        # A new generation
        g += 1
        print(f" - - - Generation: {g} - - - ")
        print(f"({time.time() - timeStart:.0f} seconds in)")

        # Select the next generation
        offspring = toolbox.select(pop, len(pop))
        # Clone the individuals (ensures no pass by reference funky business
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutations to the individuals
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if np.random.random_sample() < MatePB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        for mutant in offspring:
            if np.random.random_sample() < MutatePB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Some fitness values are now invalid, evaluate these
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Set the population to the new offspring
        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        # - - - Stats - - -

        length = len(pop)
        mean = sum(fits) / length
        q25, q50, q75 = np.quantile(fits, [0.25, 0.5, 0.75])
        zeros = fits.count(0)/len(fits) * 100


        # print(f"  Min {min(fits):.3f}")
        print(f"  Max {max(fits):.3f}")
        print(f"  Avg {mean:.3f}")
        print(f"  Quantiles - 25:{q25:.3f}, 50:{q50:.3f}, 75:{q75:.3f}")
        print(f"  Zeros {zeros:.0f} %")
        stats.append({"g": g, "avg": mean, "q25": q25, "q50": q50, "q75": q75,
                      "max": max(fits)})

    print(f"Pickling pop ({time.time() - timeStart:.0f} seconds in)")
    with open(f"population.pkl", 'wb') as popFile:
        pickle.dump(pop, popFile)
        pickle.dump(stats, popFile)

    print(f"Done ({time.time() - timeStart:.0f} seconds in)")
    return pop, stats


def viewResults(filename):

    # - - - Get data - - -
    with open(filename, 'rb') as popFile:
        pop = pickle.load(popFile)
        stats = pickle.load(popFile)

    # - - - Print fitness of last gen - - -
    fits = [ind.fitness.values[0] for ind in pop]
    index = 0
    for fit in fits:
        if fit == stats[-1]['max']:
            print(f'{colorama.Back.GREEN} {index:03d}: {fit:.3f} {colorama.Style.RESET_ALL} |', end='')
        elif fit > stats[-1]['q75']:
            print(f'{colorama.Fore.GREEN} {index:03d}: {fit:.3f} {colorama.Style.RESET_ALL} |', end='')
        elif fit > stats[-1]['q25'] + 0.001:
            print(f' {index:03d}: {fit:.3f} {colorama.Style.RESET_ALL} |', end='')
        else:
            print(f'{colorama.Fore.RED} {index:03d}: {fit:.3f} {colorama.Style.RESET_ALL} |', end='')
        index += 1
        if index % 5 == 0:
            print()

    # - - - Plot progression - - -
    fig, ax = plt.subplots()
    q50s = [stat['q50'] for stat in stats]
    q25s = [stat['q25'] for stat in stats]
    q75s = [stat['q75'] for stat in stats]
    maxs = [stat['max'] for stat in stats]
    ax.plot(q50s, color='blue')
    ax.plot(q25s, color='grey', linestyle='--')
    ax.plot(q75s, color='grey', linestyle='--')
    ax.plot(maxs, color='red')
    plt.show()

    while True:
        choice = input("Index of individual to show (enter anything but a number to quit): ")
        try:
            index = int(choice)
            showShape(pop[index])
            animate = input("Animate the figure? (y/n) ")
            if animate == 'y' or animate == 'yes' or animate == 'Y':
                poss, rots = getWalk(pop[index])
                animateWalk(pop[index], poss, rots)
        except ValueError:
            print("okay, bye :)")
            break



main(20)  # , "population.pkl")
viewResults("population.pkl")
