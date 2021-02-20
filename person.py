import faker, enums, logging
import numpy as np
import datetime as dt

class Person:
    def __init__(self):
        if isinstance(self, Nobody):
            self.name = None
            self.birthdate = None
            self.age = None
            self.state = None
        else:
            nationalities = ['en_US']
            fake = faker.Faker(nationalities)
            self.name = fake.name()
            self.birthdate = fake.date_of_birth()
            self.age = int((dt.date.today() - self.birthdate).days / 365.25)
            self.state = enums.COVIDState.SUSCEPTIBLE
            self.day_exposed = 0

    def covid_risk(self):
        if self.age < 18.0:
            return 1
        elif 18.0 <= self.age <= 35.0:
            return 2
        elif 35.0 <= self.age <= 55.0:
            return 3
        elif 55.0 <= self.age <= 75.0:
            return 4
        else: return 5

    def covid_risk_string(self):
        if self.age < 18.0:
            return 'Very Low'
        elif 18.0 <= self.age <= 35.0:
            return 'Low'
        elif 35.0 <= self.age <= 55.0:
            return 'Moderate'
        elif 55.0 <= self.age <= 75.0:
            return 'High'
        else: return 'Very High'

class Nobody(Person):
    def __init__(self):
        super().__init__()

class Individual(Person):
    def __init__(self, id, social_distancing_adherence=0, mask=enums.Mask.NONE):
        super().__init__()
        self.x = 0 # current position on the grid
        self.y = 0
        self.grid_id = id
        if social_distancing_adherence == None:
            self.social_distancing_adherence = 0.60 * np.random.random_sample() + 0.40
        else:
            self.social_distancing_adherence = social_distancing_adherence
        self.encroach_chance = 1 - self.social_distancing_adherence # Chance for this person to violate social distancing guidelines (aka walk within simulation.exposure_distance of another individual)
        if mask == None:
            mask_int = np.random.randint(0,3) # Pick a random mask
            self.mask = enums.Mask(mask_int)
        else:
            self.mask = mask

    def planned_position_random(self, max_distancex=2, max_distancey=2, max_x=100, max_y=100):
        # Pick a random position this individual plans to walk to
        # Magnitudes
        dx = np.random.randint(low=0, high=max_distancex)
        dy = np.random.randint(low=0, high=max_distancey)
        # Directions
        direction_vectors = [(0,1), (0,-1), (1,0), (-1,0)] # North, South, East, West
        chosen_direction = direction_vectors[np.random.randint(0,3)]
        new_x = self.x + (chosen_direction[0] * dx)
        new_y = self.y + (chosen_direction[1] * dy)
        # "wrap around" the new position if it is out of bounds
        if new_x < 0:
            new_x = max_x - new_x
        if new_x >= max_x:
            new_x = new_x - max_x
        if new_y < 0:
            new_y = max_y - new_y
        if new_y >= max_y:
            new_y = new_y - max_y
        return (new_x, new_y)

    def expose(self, persons, t, base_chance=0.35):
        # Expose a list of persons to COVID with the given chance of exposure (modified by mask)
        for person in persons:
            logging.debug('Checking exposure from {} to {}...'.format(self.name, person.name))
            total_exp_chance = enums.MASK_TRANSMISSION_MODIFIERS.get(self.mask) * base_chance
            logging.debug('final exposure chance: {}'.format(total_exp_chance))
            result = np.random.random(1)
            logging.debug('exposure check result: {}'.format(result))
            if result < total_exp_chance:
                if person.state == enums.COVIDState.SUSCEPTIBLE and person is not self:
                    person.state = enums.COVIDState.EXPOSED
                    person.day_exposed = t
                    logging.info('{} has infected {} with COVID-19!'.format(self.name, person.name))

    def check_infection_state(self, t, incubation_pd=4):
        day_infected = self.day_exposed + incubation_pd
        if t >= day_infected and self.state == enums.COVIDState.EXPOSED:
            self.state = enums.COVIDState.INFECTED
            logging.info('{} has become infected and can now transmit COVID'.format(self.name))