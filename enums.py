from enum import Enum

class COVIDState(Enum):
    SUSCEPTIBLE = 'susceptible'
    EXPOSED = 'exposed'
    INFECTED = 'infected'
    HOSPITALIZED = 'hospitalized'
    CRITICAL = 'critical'
    DEAD = 'dead'
    RECOVERED = 'recovered'

class Mask(Enum): # Mask types and transmission chance modifers
    NONE = 0
    CLOTH = 1
    SURGICAL = 2
    N95 = 3

MASK_TRANSMISSION_MODIFIERS = {Mask.NONE: 1.00, Mask.CLOTH: 0.60, Mask.SURGICAL: 0.25, Mask.N95: 0.07}

STATE_COLORS = {COVIDState.SUSCEPTIBLE: 'blue',
                COVIDState.EXPOSED: 'firebrick',
                COVIDState.INFECTED: 'red',
                COVIDState.HOSPITALIZED: 'darkred',
                COVIDState.CRITICAL: 'mediumvioletred',
                COVIDState.DEAD: 'black',
                COVIDState.RECOVERED: 'green'}