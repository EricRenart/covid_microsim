import faker
import numpy as np
import datetime as dt
import dateutils as du
import enums

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
    def __init__(self):
        super().__init__()
        self.x = 0 # current position on the grid
        self.y = 0
