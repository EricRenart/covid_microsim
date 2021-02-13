from person import Person, Individual
from grid import Grid

def test_generator(n=100):
    for n in range(0,n-1):
        fake_person = Person()
        print('Name: {} Age: {} DOB: {} COVID risk: {}'.format(fake_person.name, fake_person.age, fake_person.birthdate, fake_person.covid_risk_string()))

def test_grid(n_individuals=0):
    grid = Grid()
    if n_individuals > 0:
        for i in range(0, n_individuals-1):
            grid.add_individual_at_random_location(Individual())
    print(grid)

test_grid(50)
