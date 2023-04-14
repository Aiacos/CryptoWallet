#    This file is part of DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.

from eth_account import Account
from web3 import Web3, HTTPProvider
import array
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

import multiprocessing

import wallet

pool = multiprocessing.Pool()



pattern = '0x324e2D42D7B65E5574787C331DfaA29d2Dead666' #0x324e2d42d7b65e5574787c331dfaa29d2dead666

def generateAccount():
    private_key, public_key, mnemonic = wallet.generateAccount('fast')

    return [x for x in private_key]

print('Creator')

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
#toolbox.register("map", pool.map)

# Attribute generator
toolbox.register("attr_str", generateAccount)

print('Structure initializers')

# Structure initializers
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_str)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def fitness(individual):
    counter = 0

    pri_key = ""
    pri_key = pri_key.join(individual)
    print("Private: ", pri_key)
    try:
        acct = Account.from_key(pri_key)
        address = acct.address
        print("Address: ",address)
        for c, i in zip(address, pattern.lower()):
            if c == i:
                counter = counter + 1

        return counter,
    except:
        return 0,

toolbox.register("evaluate", fitness)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    random.seed(64)
    POP_SIZE = 100

    pop = toolbox.population(n=1000)
    #ind = creator.Individual(toolbox.attr_str())
    #pop = [creator.Individual(toolbox.attr_str()) for _ in range(POP_SIZE)]
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.5, ngen=500,
                                   stats=stats, halloffame=hof, verbose=True)

    return pop, log, hof

if __name__ == "__main__":
    pop, log, hof = main()

    s = ""
    p_key = s.join(hof[0])
    acct = Account.from_key(p_key)
    address = acct.address
    print('HoF: ', p_key, address)