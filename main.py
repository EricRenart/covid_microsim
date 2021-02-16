from person import Person, Individual
import numpy as np
import seaborn as sns
from simulation import Simulation
from matplotlib import pyplot as pp
from matplotlib.animation import FuncAnimation, FFMpegWriter
import logging, sys

def animation_step(i): # Animation update function
    x = frames[i][0]
    y = frames[i][1]
    xy = np.c_[x,y]
    scatter.set_offsets(xy)
    scatter.set_color(frames[i][2])
    ax.set_title('COVID simulation, {} individuals, t={}'.format(sim.population(), sim.t))
    return scatter,

# MAIN PROGRAM
sns.set()

pop = 250
length = 100

stream = logging.StreamHandler(sys.stdout)
file = logging.FileHandler(filename='output.txt', mode='w')
logging.basicConfig(level=logging.INFO, handlers=(stream, file)) # set up an output file and also print to console
print('Starting simulation with population of {} and length {}...'.format(pop, length))

# Create simulation with grid
sim = Simulation()

# Set up initial scatterplot
fig, ax = pp.subplots(figsize=(12, 12))
ax.set_xlim(0, sim.size_x)
ax.set_ylim(0, sim.size_y)
ax.set_title('COVID simulation, {} individuals, t=0'.format(sim.population()))

frames = sim.run(pop=pop, length=length)
scatter, = ax.scatter(frames[0][0], frames[0][1], c=frames[0][2], s=5, lw=1),

# Set up animation
animation = FuncAnimation(fig, animation_step, interval=100, blit=True)
pp.show()

# Save a video
writer = FFMpegWriter(fps=20, bitrate=1800)
animation.save('simulation.mp4', writer=writer)