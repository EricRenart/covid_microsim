from enum import Enum

class COVIDState(Enum):
    SUSCEPTIBLE = 'susceptible'
    EXPOSED = 'exposed'
    INFECTED = 'infected'
    HOSPITALIZED = 'hospitalized'
    CRITICAL = 'critical'
    DEAD = 'dead'
    RECOVERED = 'recovered'

STATE_COLORS = {COVIDState.SUSCEPTIBLE: 'blue',
                COVIDState.EXPOSED: 'firebrick',
                COVIDState.INFECTED: 'red',
                COVIDState.HOSPITALIZED: 'darkred',
                COVIDState.CRITICAL: 'mediumvioletred',
                COVIDState.DEAD: 'black',
                COVIDState.RECOVERED: 'green'}