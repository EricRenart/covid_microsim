import numpy as np
from matplotlib import pyplot as pp
from matplotlib.animation import FuncAnimation
from person import Nobody, Individual, Person
from enums import COVIDState, STATE_COLORS
import logging

class Simulation():

    def __init__(self, size_x=100, size_y=100):
        self.length = 0
        self.size_x = size_x
        self.size_y = size_y
        self.t = 0
        self.grid = np.ndarray((size_x, size_y), dtype=Person)
        self.grid.fill(Nobody())
        self.next_available_id = 1
        self.exposure_distance = 3 # distance individuals must be within each other to get exposed. Individuals will try to stay greater than this value apart from each other on the grid, based on their social distancing adherece

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
        self.length = length
        for i in range(0, pop):
            self.add_individual_at_random_location() # Add initial individuals to grid
        logging.info('Running COVID-19 microsimulation with population of {}...'.format(self.population()))
        logging.info('Initial Conditions:\n')
        logging.info(self.list_individuals())
        logging.info('Starting simulation.')
        step_plots = [] # Set up list of plots to animate
        for i in range(0, length-1):
            self.step()
            current_plot = self.get_plot_data()
            step_plots.append(current_plot) # Append the current plot to the list of plots
        logging.info('Simulation Complete!')
        logging.info('Final Results by individual:')
        logging.info(self.list_individuals())
        return step_plots # Return list of frames to animate through

    def step(self):
        self.t += 1 # Advance the simulation by one time unit
        self.update_positions() # Have each individual walk a random distance, avoiding encroaching within exposure_distance based on their social distancing modifier
        for individual in self.individuals(): # Perform exposure check on all individuals within exposure_distance
            if individual.state == COVIDState.INFECTED:
                close_individuals = self.individuals_within_social_distance(individual.x, individual.y)
                individual.expose(close_individuals, self.t)
            individual.check_infection_state(self.t, incubation_pd=4) # Check whether they are infected based on the incubation period
        self.update_counts() # Update counts of individual states

    def list_individuals(self):
        # List the individuals in the grid and their positions
        list = ''
        for i in range(0, self.size_x - 1):
            for j in range(0, self.size_y - 1):
                if isinstance(self.grid[i,j], Individual):
                    ind = self.grid[i,j]
                    list = list + '| {}. {} (age {}) | [{},{}] | {} | Mask: {} | SD adherence: {} | \n'.format(ind.grid_id, ind.name, ind.age, i, j, ind.state, ind.mask, ind.social_distancing_adherence)
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

    def update_positions(self, max_walk_distance=3):
        individuals = self.individuals()
        for individual in individuals:
            max_x = self.size_x
            max_y = self.size_y
            (current_x, current_y) = (individual.x, individual.y)
            (planned_x, planned_y) = individual.planned_position_random(max_distancex=max_walk_distance, max_distancey=max_walk_distance, max_x=max_x, max_y=max_y)
            planned_encroachment = len(self.individuals_within_social_distance(planned_x, planned_y)) > 0 # Are there individuals within social distance?
            if planned_encroachment:
                if np.random.rand(1) < individual.encroach_chance: # If the individual decides to violate social distancing
                    logging.info('{} decided to violate social distancing'.format(individual.name)) # violate social distancing anyway
                else:
                    (planned_x, planned_y) = individual.planned_position_random(max_distancex=max_walk_distance, max_distancey=max_walk_distance, max_x=max_x, max_y=max_y) # individual decided to keep social distance this time, pick a new position

            # Update the actual grid
            self.grid[current_x, current_y] = Nobody() # clear old position
            individual.x = planned_x # update individuals position
            individual.y = planned_y
            self.grid[planned_x, planned_y] = individual # set new grid position

    def update_counts(self):
        self.reset_counts()
        for individual in self.individuals():
            state = individual.state
            if state == COVIDState.SUSCEPTIBLE:
                self.susceptible += 1
            elif state == COVIDState.EXPOSED:
                self.exposed += 1
            elif state == COVIDState.INFECTED:
                self.infected += 1
            elif state == COVIDState.HOSPITALIZED:
                self.hospitalized += 1
            elif state == COVIDState.CRITICAL:
                self.critical += 1
            elif state == COVIDState.DEAD:
                self.dead += 1
            elif state == COVIDState.RECOVERED:
                self.recovered += 1

    def reset_counts(self):
        self.susceptible = 0
        self.exposed = 0
        self.infected = 0
        self.hospitalized = 0
        self.critical = 0
        self.dead = 0
        self.recovered = 0

    def individuals_within_social_distance(self, x, y):
        # Get a list of individuals within social distance of the given point on the grid
        close_individuals = []
        for i in range(0, self.size_x-1):
            for j in range(0, self.size_y-1):
                point = self.grid[i,j]
                if isinstance(point, Individual):
                    dx = np.abs(x - i)
                    dy = np.abs(y - j)
                    dist = np.hypot(dx, dy)
                    if dist <= self.exposure_distance and dist != 0.0:
                        close_individuals.append(self.grid[i,j])
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

    def get_plot_data(self):
        x_positions = []
        y_positions = []
        state_colors = []
        for ind in self.individuals():
            x_positions.append(ind.x)
            y_positions.append(ind.y)
            state_colors.append(STATE_COLORS.get(ind.state))
        return (x_positions, y_positions, state_colors)