import numpy as np
from matplotlib import pyplot as pp
from person import Nobody, Individual, Person
from enums import COVIDState, STATE_COLORS

class Simulation():

    def __init__(self, size_x=1000, size_y=1000):
        self.size_x = size_x
        self.size_y = size_y
        self.t = 0
        self.grid = np.ndarray((size_x, size_y), dtype=Person)
        self.grid.fill(Nobody())

    def __str__(self):
        size = self.grid.size
        population = self.population()
        ind_list = self.list_individuals()
        return '{}x{} grid, {} total slots, \n{} individuals present: \n{}'.format(self.size_x, self.size_y, size, population, ind_list)

    def list_individuals(self):
        # List the individuals in the grid and their positions
        list = ''
        n = 1
        for i in range(0, self.size_x - 1):
            for j in range(0, self.size_y - 1):
                if isinstance(self.grid[i,j], Individual):
                    ind = self.grid[i,j]
                    list = list + '{}. {} (age {}) at [{},{}] ({}) \n'.format(n, ind.name, ind.age, i, j, ind.state)
                    n += 1
        return list

    def individuals(self):
        """
        Get a list of all Individuals in the grid and their coordinates
        """
        list = []
        for i in range(0, self.size_x - 1):
            for j in range(0, self.size_y - 1):
                if isinstance(self.grid[i,j], Individual):
                    list.append(self.grid[i,j])
        return list

    def population(self):
        n = 0 # start a counter
        # count the number of Individuals in the grid
        for i in range(0, self.size_x - 1):
            for j in range(0, self.size_y - 1):
                if isinstance(self.grid[i,j], Individual):
                    n += 1
        return n

    def add_individual_at_random_location(self, individual):
        coords = self.random_coordinates() # Generate the random location
        while self.slot_occupied(coords[0], coords[1]): # if the chosen slot is already occupied
            coords = self.random_coordinates()  # keep searching for an open slot
        individual.x = coords[0] # set individuals's coords
        individual.y = coords[1]
        if self.population() == 0:
            individual.state = COVIDState.EXPOSED # first person is always exposed
        self.grid[coords[0], coords[1]] = individual # add the individual to the slot

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

    def plot(self):
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