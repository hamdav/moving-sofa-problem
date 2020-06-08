from deap import base
from deap import creator
from deap import tools

import time
import numpy as np
import matplotlib.pyplot as plt
import pickle
import multiprocessing as mp

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
def evalByArea(individual):
    if not individual.valid:
        return 0,
    elif not shapeIsValid(individual):
        return 0,
    else:
        return individual.area,


def evalByValidity(individual):
    if not individual.valid:
        return 0,
    elif not shapeIsValid(individual):
        return 0,
    else:
        return individual.area,


def evaluateInd(individual, goodTimes=False):
    if not goodTimes:
        return evalByArea(individual)
    else:
        return evalByValidity(individual)


# Let's define som genetic operators
toolbox.register('evaluate', evaluateInd)
toolbox.register('mate', Shape.mate)
toolbox.register('mutate', Shape.mutateInPlace)
toolbox.register('select', tools.selTournament, tournsize=2)


# Now we write the main program
def main(maxGen, filename=None):
    # - - - Initial setup - - -
    # Create multiprocessing pool
    pool = mp.Pool(processes=1)

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
    fitnesses = list(pool.map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # Probability of mating and mutation
    MatePB, MutatePB = 0.5, 1.0

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
        offspring = toolbox.select(pop, len(pop)-1)
        # Remember the best guy
        topDog = pop[np.argmax(fits)]
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

        # Add the top dog
        offspring.append(topDog)

        # If times are good (happens for ten generations every 20 generations)
        # then don't select based on area, just abillity to pass the corner
        goodTimes = (g % 20) >= 10
        timesAreChanging = (g % 10) == 0

        # If times are changing from good to bad or the other way around
        # All fitnesses must be recalculated.
        if timesAreChanging:
            for ind in offspring:
                del ind.fitness.values

        # Calculate fitnesses (some may already be calculated, in that case
        # there is no need to recalculate them)
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = pool.map(lambda ind: toolbox.evaluate(ind, goodTimes),
                             invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Set the population to the new offspring
        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        # - - - Stats - - -

        length = len(pop)
        mean = sum(fits) / length
        quantiles = np.quantile(fits, np.arange(0.1, 1.0, 0.1))
        zeros = fits.count(0)/len(fits) * 100


        # print(f"  Min {min(fits):.3f}")
        print(f"  Max {max(fits):.3f}")
        print(f"  Avg {mean:.3f}")
        print(f"  Quantiles - 20:{quantiles[1]:.3f}, 50:{quantiles[4]:.3f}, 80:{quantiles[7]:.3f}")
        print(f"  Zeros {zeros:.0f} %")
        stats.append({"g": g, "avg": mean, "qs": quantiles,
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
        elif fit > stats[-1]['qs'][7]:
            print(f'{colorama.Fore.GREEN} {index:03d}: {fit:.3f} {colorama.Style.RESET_ALL} |', end='')
        elif fit > stats[-1]['qs'][1] + 0.001:
            print(f' {index:03d}: {fit:.3f} {colorama.Style.RESET_ALL} |', end='')
        else:
            print(f'{colorama.Fore.RED} {index:03d}: {fit:.3f} {colorama.Style.RESET_ALL} |', end='')
        index += 1
        if index % 5 == 0:
            print()

    # - - - Plot progression - - -
    fig, ax = plt.subplots()
    maxs = [stat['max'] for stat in stats]
    qs = [stat['qs'] for stat in stats]

    ax.plot(qs, color='grey', linestyle='-')
    ax.plot([q[4] for q in qs], color='blue', linestyle='-')
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



#main(20, 'population.pkl')  # , "population.pkl")
viewResults("pop.pkl")
