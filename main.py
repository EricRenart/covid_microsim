from person import Person, Individual
from simulation import Simulation

def test_generator(n=100):
    for n in range(0,n-1):
        fake_person = Person()
        print('Name: {} Age: {} DOB: {} COVID risk: {} State: {}'.format(fake_person.name, fake_person.age, fake_person.birthdate, fake_person.covid_risk_string(). fake_person.state))

def test_grid(n_individuals=0):
    sim = Simulation()
    if n_individuals > 0:
        for i in range(0, n_individuals-1):
            sim.add_individual_at_random_location(Individual())
    sim.plot()

test_grid(50)
