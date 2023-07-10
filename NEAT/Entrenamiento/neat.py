import neat

from flappy_gen import main2, mainGame


def eval_fitness(genomes, config):
    for genome_id, genome in genomes:
        # Evaluate the fitness of each genome
        # Assign a fitness score to the genome
        genome.fitness = ...


config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'path/to/config-file')

population = neat.Population(config)

reporter = neat.StdOutReporter(True)
population.add_reporter(reporter)

winner = population.run(eval_fitness, 100)

best_genome = winner