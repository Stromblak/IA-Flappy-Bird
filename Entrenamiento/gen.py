from flappy_gen import *
from red import NODOS, CAPAS
import random
import os
import operator

POBLACION = 10
MUTACION = 10
DELTA = 0.05
MINFITNESS = 2500
HIJOS = 2
USARPESOS = False


class Pajaro:
	def __init__(self, archivo):
		self.fitness = 0

		if archivo == " ":

			self.pesos = []
			for i in range(CAPAS-1):
				self.pesos.append( [] )
				for j in range(NODOS[i+1]):
					self.pesos[i].append( np.zeros(NODOS[i], dtype=float) )

					for k in range(NODOS[i]):
						self.pesos[i][-1][k] = random.uniform(0, 1)


	def hijo(self, p1, p2):
		for i in range(CAPAS-1):
			for j in range(NODOS[i+1]):
				for k in range(NODOS[i]):
					self.pesos[i][j][k] = random.choice([p1.pesos[i][j][k], p2.pesos[i][j][k]])

		self.mutar()

	def mutar(self):
		camino = []
		for i in range(CAPAS):
			camino.append( random.randint(0, NODOS[i]-1) )

		delta = random.choice([-DELTA, DELTA])
		for i in range(1, CAPAS):
			nuevo = self.pesos[i-1][ camino[i] ][ camino[i-1] ] + delta

			if delta > 0:
				self.pesos[i-1][ camino[i] ][ camino[i-1] ] = min(1, nuevo)

			else:
				self.pesos[i-1][ camino[i] ][ camino[i-1] ] = max(0, nuevo)		

	def guardar(self, archivo):
		if self.fitness < MINFITNESS:
			return
				
		f = open(archivo + "-" + str(self.fitness) + ".txt", 'w')

		for i in range(CAPAS-1):
			for j in range(NODOS[i+1]):
				f.write( " ".join( [str(v) for v in self.pesos[i][j]]) + "\n")

		f.close()


def algGenetico():
	main2()
	genPajaro = 0

	# Creacion poblacion
	if USARPESOS:
		dir_list = os.listdir("./pesos")
		pajaros = [ Pajaro( "./pesos/" + dir_list[i] ) for i in range(len(dir_list)) ]
		pajaros.extend( [ Pajaro(" ") for i in range(len(dir_list), POBLACION) ])
	
	else:
		pajaros = [ Pajaro(" ") for i in range(POBLACION) ]


	while True:
		# Calculo fitness
		fitness = mainGame(POBLACION, pajaros)
		for i in range(POBLACION):
			pajaros[i].fitness = fitness[i]

		# Descedencia
		pajaros.sort(key=operator.attrgetter('fitness'))
		pajaros.reverse()
		
		for i in range( int(HIJOS/2) ):
			pajaros[POBLACION-1 - i  ].hijo(pajaros[i], pajaros[i+1])
			pajaros[POBLACION-1 - i-1].hijo(pajaros[i], pajaros[i+1])

		# Mutacion
		for i in range(POBLACION):
			if MUTACION < random.randint(0, 100):
				pajaros[i].mutar()

			pajaros[i].guardar("pesos/peso" + str(genPajaro))
			genPajaro += 1


algGenetico()