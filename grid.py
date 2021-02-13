import numpy as np
from person import Nobody, Individual, Person

class Grid():

    def __init__(self, size_x=1000, size_y=1000):
        self.size_x = size_x
        self.size_y = size_y
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
                    list = list + '{}. {} (age {}) at [{},{}] \n'.format(n, ind.name, ind.age, i, j)
                    n += 1
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
