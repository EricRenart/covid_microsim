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
    def __init__(self, id, social_distancing_adherence=None, mask=None):
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

    def planned_position(self, direction, distancex=1, distancey=1):
        assert isinstance(direction, enums.Direction)
        new_x = self.x + (enums.MOVEMENT_DELTAS.get(direction)[0] * distancex)
        new_y = self.y + (enums.MOVEMENT_DELTAS.get(direction)[1] * distancey)
        return (new_x, new_y) # Re-indexing to grid coordinates

    def planned_position_random(self, max_distancex=5, max_distancey=5, max_x=100, max_y=100):
        # Pick a random position this individual plans to walk to
        dx = np.random.randint(low=0, high=max_distancex+1)
        dy = np.random.randint(low=0, high=max_distancey+1)
        direction = enums.DIRECTION_BY_ID.get(np.random.randint(0,3))
        position = self.planned_position(direction, distancex=dx, distancey=dy)
        # make sure the new position is within bounds
        while (position[0] < 0) or (position[1] < 0) or (position[0] >= max_x) or (position[1] >= max_y): # If out of bounds keep generating new positions until one is within bounds
            position = self.planned_position_random(max_distancex, max_distancey, max_x, max_y)
        return position

    def expose(self, persons, t, base_chance=0.20):
        # Expose a list of persons to COVID with the given chance of exposure (modified by mask)
        logging.debug('Checking exposure from {} to {}'.format(self.name, [person.name for person in persons]))
        for person in persons:
            total_exp_chance = enums.MASK_TRANSMISSION_MODIFIERS.get(self.mask) * base_chance
            rand = np.random.random(1)
            if rand < total_exp_chance:
                if person.state == enums.COVIDState.SUSCEPTIBLE and person is not self:
                    person.state = enums.COVIDState.EXPOSED
                    person.day_exposed = t
                    logging.info('{} has infected {} with COVID-19!'.format(self.name, person.name))

    def check_infection_state(self, t, incubation_pd=4):
        day_infected = self.day_exposed + incubation_pd
        if t >= day_infected and self.state == enums.COVIDState.EXPOSED:
            self.state = enums.COVIDState.INFECTED
            logging.info('{} has become infected and can now transmit COVID'.format(self.name))