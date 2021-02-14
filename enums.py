from enum import Enum

class COVIDState(Enum):
    SUSCEPTIBLE = 'susceptible'
    EXPOSED = 'exposed'
    INFECTED = 'infected'
    HOSPITALIZED = 'hospitalized'
    CRITICAL = 'critical'
    DEAD = 'dead'
    RECOVERED = 'recovered'

class Direction(Enum): # Directions to walk in on grid
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4

class Mask(Enum): # Mask types and transmission chance modifers
    NONE = 0
    CLOTH = 1
    SURGICAL = 2
    N95 = 3

MASK_TRANSMISSION_MODIFIERS = {Mask.NONE: 0.00, Mask.CLOTH: 0.40, Mask.SURGICAL: 0.70, Mask.N95: 0.90}

DIRECTION_BY_ID = {0: Direction.NORTH,
                   1: Direction.EAST,
                   2: Direction.SOUTH,
                   3: Direction.WEST}

MOVEMENT_DELTAS = {Direction.NORTH: (0,1),
                   Direction.SOUTH: (0,-1),
                   Direction.EAST: (1,0),
                   Direction.WEST: (-1,0)}

STATE_COLORS = {COVIDState.SUSCEPTIBLE: 'blue',
                COVIDState.EXPOSED: 'firebrick',
                COVIDState.INFECTED: 'red',
                COVIDState.HOSPITALIZED: 'darkred',
                COVIDState.CRITICAL: 'mediumvioletred',
                COVIDState.DEAD: 'black',
                COVIDState.RECOVERED: 'green'}