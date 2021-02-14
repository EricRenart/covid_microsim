from person import Person, Individual
from simulation import Simulation
import os, logging, sys

def run_simulation(pop=15, length=25):
    stream = logging.StreamHandler(sys.stdout)
    file = logging.FileHandler(filename='output.txt', mode='w')
    logging.basicConfig(level=logging.INFO, handlers=(stream, file)) # set up an output file and also print to console

    sim = Simulation()
    print('Starting simulation with population of {} and length {}...'.format(pop, length))
    output = sim.run(pop=pop, length=length)

run_simulation()
