import os
from flappy_gen import main2, mainGame
import neat
import statistics

xor_inputs = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
xor_outputs = [(0.0,), (1.0,), (1.0,), (0.0,)]

f = open("calidad.txt", "w")

def eval_genomes(genomes, config):
	nets = []
	for genome_id, genome in genomes:
		nets.append( neat.nn.FeedForwardNetwork.create(genome, config) )

	fitness, dist = mainGame(nets)

	print(statistics.mean(fitness), max(fitness))
	f.write(str(statistics.mean(fitness)) + " " + str(max(fitness)) + "\n")

	i = 0
	for genome_id, genome in genomes:
		genome.fitness = fitness[i]
		i += 1


def run(config_file):
	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
						neat.DefaultSpeciesSet, neat.DefaultStagnation,
						config_file)

	p = neat.Population(config)

	#p.add_reporter(neat.StdOutReporter(True))
	#stats = neat.StatisticsReporter()
	#p.add_reporter(stats)
	#p.add_reporter(neat.Checkpointer(100))

	winner = p.run(eval_genomes, 300)

	# Display the winning genome.
	print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
	main2()
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, 'neat_config.ini')

	run(config_path)