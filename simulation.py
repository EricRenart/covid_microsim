import numpy as np
from matplotlib import pyplot as pp
from person import Nobody, Individual, Person
from enums import COVIDState, STATE_COLORS
import logging

class Simulation():

    def __init__(self, size_x=100, size_y=100):
        self.size_x = size_x
        self.size_y = size_y
        self.t = 0
        self.grid = np.ndarray((size_x, size_y), dtype=Person)
        self.grid.fill(Nobody())
        self.next_available_id = 1
        self.exposure_distance = 6 # distance individuals must be within each other to get exposed. Individuals will try to stay greater than this value apart from each other on the grid, based on their social distancing adherece

        # Number of people in each state
        self.susceptible = 0
        self.infected = 0
        self.exposed = 0
        self.hospitalized = 0
        self.critical = 0
        self.dead = 0
        self.recovered = 0

    def __str__(self):
        size = self.grid.size
        population = self.population()
        ind_list = self.list_individuals()
        return '{}x{} grid, {} total slots, \n{} individuals present: \n{}'.format(self.size_x, self.size_y, size, population, ind_list)

    def run(self, pop=50, length=100):
        for i in range(0, pop):
            self.add_individual_at_random_location() # Add initial individuals to grid
        logging.warning('Running COVID-19 microsimulation with population of {}...'.format(self.population()))
        logging.warning('Initial Conditions:\n')
        logging.warning(self.list_individuals())
        self.plot('initial_results.png')
        logging.warning('Starting simulation.')
        for i in range(0, length-1):
            self.step()
            logging.warning('t = {}, susc = {}, exp = {}, inf = {}, hosp = {}, crit = {}, dead = {}, recov={}'.format(self.t, self.susceptible, self.exposed, self.infected, self.hospitalized, self.critical, self.dead, self.recovered))
        logging.warning('SIMULATION COMPLETE!')
        logging.warning('Final Results by individual:')
        logging.warning(self.list_individuals())
        self.plot('final_results.png')
        return self.list_individuals()

    def step(self):
        self.t += 1 # Advance the simulation by one time unit
        self.update_positions() # Have each individual walk a random distance, avoiding encroaching within exposure_distance based on their social distancing modifier
        for individual in self.individuals(): # Perform exposure check on all individuals within exposure_distance
            close_individuals = self.individuals_within_social_distance(individual.x, individual.y)
            individual.expose(close_individuals)
        self.update_counts() # Update counts of individual states


    def list_individuals(self):
        # List the individuals in the grid and their positions
        list = ''
        for i in range(0, self.size_x - 1):
            for j in range(0, self.size_y - 1):
                if isinstance(self.grid[i,j], Individual):
                    ind = self.grid[i,j]
                    list = list + '{}. {} (age {}) at [{},{}] ({}) Mask: {} SD adherence: {} \n'.format(ind.grid_id, ind.name, ind.age, i, j, ind.state, ind.mask, ind.social_distancing_adherence)
        return list

    def individuals(self):
        #Get a list of all Individuals in the grid and their coordinates
        list = []
        for i in range(0, self.size_x - 1):
            for j in range(0, self.size_y - 1):
                if isinstance(self.grid[i,j], Individual):
                    list.append(self.grid[i,j])
        return list

    def query_grid_by_id(self, id):
        # Given a grid id, return the corresponding individual and their position on the grid
        for i in range(0, self.size_x - 1):
            for j in range(0, self.size_y - 1):
                if isinstance(self.grid[i,j], Individual):
                    individual = self.grid[i,j]
                    if individual.grid_id == id:
                        return individual

    def population(self):
        return len(self.individuals())

    def update_positions(self, max_walk_distance=5):
        individuals = self.individuals()
        for individual in individuals:
            old_x = individual.x
            old_y = individual.y
            max_x = self.size_x
            max_y = self.size_y
            (planned_x, planned_y) = individual.planned_position_random(max_distancex=max_walk_distance, max_distancey=max_walk_distance, max_x=max_x, max_y=max_y)
            planned_encroachment = len(self.individuals_within_social_distance(planned_x, planned_y)) > 0 # Are there individuals within social distance?
            if planned_encroachment:
                if np.random.rand(1) < individual.encroach_chance: # If the individual decides to violate social distancing
                    pass # violate social distancing anyway
                else:
                    (planned_x, planned_y) = individual.planned_position_random(max_distancex=max_walk_distance, max_distancey=max_walk_distance, max_x=max_x, max_y=max_y) # individual decided to keep social distance this time, pick a new position
            # update position on grid
            self.grid[old_x, old_y] = Nobody() # clear old position
            self.grid[individual.x, individual.y] = individual # set new grid position

    def update_counts(self):
        for individual in self.individuals():
            state = individual.state
            if state == COVIDState.EXPOSED:
                self.susceptible -= 1
                self.exposed += 1
            elif state == COVIDState.INFECTED:
                self.exposed -= 1
                self.infected += 1
            elif state == COVIDState.HOSPITALIZED:
                self.infected -= 1
                self.hospitalized += 1
            elif state == COVIDState.CRITICAL:
                self.hospitalized -= 1
                self.critical += 1
            elif state == COVIDState.DEAD:
                self.critical -= 1
                self.dead += 1

    def individuals_within_social_distance(self, x, y):
        # Get a list of individuals within social distance of given coords on grid
        grid_population = self.individuals()
        close_individuals = []
        for individual in grid_population:
            for i in range(self.size_x - 1):
                for j in range(self.size_y - 1):
                    point = self.grid[i,j]
                    if isinstance(point, Individual):
                        dx = np.abs(x - point.x)
                        dy = np.abs(y - point.y)
                        # diagonals coming soon
                        if dx < self.exposure_distance or dy < self.exposure_distance:
                            close_individuals.append(individual)
        return close_individuals

    def add_individual_at_random_location(self):
        coords = self.random_coordinates() # Generate the random location
        while self.slot_occupied(coords[0], coords[1]): # if the chosen slot is already occupied
            coords = self.random_coordinates()  # keep searching for an open slot
        individual = Individual(self.next_available_id)
        individual.x = coords[0] # set individuals's coords
        individual.y = coords[1]
        if self.population() == 0:
            individual.state = COVIDState.EXPOSED # first person is always exposed
        self.grid[coords[0], coords[1]] = individual # add the individual to the slot
        self.next_available_id += 1

    def random_coordinates(self):
        return (np.random.randint(0, self.size_x), np.random.randint(0, self.size_y))

    def slot_occupied(self, x, y):
        if isinstance(self.grid[x, y], Individual):
            return True
        elif isinstance(self.grid[x, y], Nobody):
            return False
        else:
            raise TypeError('slot is occupied by an unauthorized data type: {}'.format(type(self.grid[x, y])))

    '''
    Plotting methods
    '''

    def plot(self, fname):
        fig, ax = pp.subplots(figsize=(16,16))
        individuals = self.individuals()
        n = self.population()
        cx = []
        cy = []
        cstate_color = []
        for ind in individuals:
            cx.append(ind.x)
            cy.append(ind.y)
            cstate_color.append(STATE_COLORS.get(ind.state))
        ax.scatter(cx, cy, c=cstate_color, s=3, alpha=1.0)
        ax.xaxis.set_label('x')
        ax.yaxis.set_label('y')
        ax.set_title('{} individuals at random positions (t = {})'.format(n, self.t))
        pp.show()
        pp.savefig(fname, dpi=300)