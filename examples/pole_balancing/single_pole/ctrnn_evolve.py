'''
Single-pole balancing experiment using a continuous-time recurrent neural network (CTRNN).
'''

from __future__ import print_function
import os
import pickle
from cart_pole import discrete_actuator_force
from fitness import evaluate_population
from neat import ctrnn, population, visualize
from neat.config import Config


# Use the CTRNN network phenotype and the discrete actuator force function.
def fitness_function(genomes):
    evaluate_population(genomes, ctrnn.create_phenotype, discrete_actuator_force)


# Load the config file, which is assumed to live in
# the same directory as this script.
local_dir = os.path.dirname(__file__)
config = Config(os.path.join(local_dir, 'ctrnn_config'))
config.node_gene_type = ctrnn.CTNodeGene

pop = population.Population(config)
pop.epoch(fitness_function, 2000, report=1, save_best=0)

# Save the winner.
print('Number of evaluations: {0:d}'.format(pop.total_evaluations))
winner = pop.most_fit_genomes[-1]
with open('ctrnn_winner_genome', 'wb') as f:
    pickle.dump(winner, f)

print(winner)

# Plot the evolution of the best/average fitness.
visualize.plot_stats(pop, ylog=True, filename="ctrnn_fitness.svg")
# Visualizes speciation
visualize.plot_species(pop, filename="ctrnn_speciation.svg")
# Visualize the best network.
visualize.draw_net(winner, view=True, filename="ctrnn_winner.gv")