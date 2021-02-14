from person import Person, Individual
from simulation import Simulation
import os, logging, sys

def test_generator(n=100):
    for n in range(0,n-1):
        fake_person = Person()
        print('Name: {} Age: {} DOB: {} COVID risk: {} State: {}'.format(fake_person.name, fake_person.age, fake_person.birthdate, fake_person.covid_risk_string(). fake_person.state))

def run_simulation(pop=10, length=25):
    stream = logging.StreamHandler(sys.stdout)
    file = logging.FileHandler(filename='output.txt', mode='w')
    logging.basicConfig(level=logging.INFO, handlers=(stream, file)) # set up an output file and also print to console

    sim = Simulation()
    print('Starting simulation with population of {} and length {}...'.format(pop, length))
    output = sim.run(pop=pop, length=length)

run_simulation()
