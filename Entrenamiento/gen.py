from flappy_gen import *
from red import NODOS, CAPAS
import random
import os
import operator
import statistics

POBLACION = 1000
MUTACIONCAMINO = 0.9
MUTACIONCONEXION = 0.0
MUTACIONBIAS = 0.0
MUTACIONACEPTACION = 0.1

DELTA = 0.05
DELTABIAS = 1

MINFITNESS = 2500
HIJOS = int(POBLACION*0.1)
USARPESOS = False
WMIN = -1
WMAX = 1


class Pajaro:
	def __init__(self, archivo):
		self.fitness = 0

		self.pesos = [ [] ]
		for i in range(1, CAPAS):
			self.pesos.append( [] )

			for j in range(NODOS[i]):
				self.pesos[i].append( np.zeros(NODOS[i-1], dtype=float) )

				for k in range(NODOS[i-1]):
					self.pesos[i][-1][k] = random.uniform(WMIN, WMAX)

		self.pesos.append(1)

		self.bias = [ [] ]
		for i in range(1, CAPAS):
			self.bias.append( [] )
			for j in range(NODOS[i]):
				self.bias[i].append(0)

	def hijo(self, p1, p2):
		for i in range(1, CAPAS):
			for j in range(NODOS[i]):
				for k in range(NODOS[i-1]):
					self.pesos[i][j][k] = random.choice([p1.pesos[i][j][k], p2.pesos[i][j][k]])

		self.pesos[-1] = random.choice([p1.pesos[-1], p2.pesos[-1]])

		for i in range(1, CAPAS):
			for j in range(NODOS[i]):
				self.bias[i][j] = random.choice([p1.bias[i][j], p2.bias[i][j]])

		self.mutarCamino()
		self.mutarConexion()
		self.mutarBias()

		self.fitness = 0

	def mutarCamino(self):
		camino = []
		for i in range(CAPAS):
			camino.append( random.randint(0, NODOS[i]-1) )

		delta = random.uniform(-DELTA, DELTA)
		
		for i in range(1, CAPAS):
			nuevo = self.pesos[i][ camino[i] ][ camino[i-1] ] + delta

			if delta > 0:
				self.pesos[i][ camino[i] ][ camino[i-1] ] = min(WMAX, nuevo)

			else:
				self.pesos[i][ camino[i] ][ camino[i-1] ] = max(WMIN, nuevo)	

	def mutarConexion(self):
		capa  = random.randint(1, CAPAS-1)
		nodoCapa = random.randint(0, NODOS[capa]-1)
		nodoAnterior = random.randint(0, NODOS[capa-1]-1)

		delta = random.uniform(-DELTA, DELTA)		
		nuevo = self.pesos[capa][nodoCapa][nodoAnterior] + delta

		if delta > 0:
			self.pesos[capa][nodoCapa][nodoAnterior] = min(WMAX, nuevo)
		else:
			self.pesos[capa][nodoCapa][nodoAnterior] = max(WMIN, nuevo)	
	
	def mutarActivacion(self):
		delta = random.uniform(-0.5, 0.5)		
		self.pesos[-1] = max(1, self.pesos[-1] + delta)

	def mutarBias(self):
		capa  = random.randint(1, CAPAS-1)
		nodoCapa = random.randint(0, NODOS[capa]-1)
		self.bias[capa][nodoCapa] = random.uniform(-DELTABIAS, DELTABIAS)	
	
	def guardar(self, archivo):
		if self.fitness < MINFITNESS:
			return
				
		f = open(archivo + "-" + str(self.fitness) + ".txt", 'w')

		for i in range(1, CAPAS):
			for j in range(NODOS[i]):
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

		print(statistics.mean(fitness), max(fitness))

		# Descedencia
		pajaros.sort(key=operator.attrgetter('fitness'))
		pajaros.reverse()
		
		for i in range(HIJOS):
			p1 = random.randint(0, HIJOS-1)
			p2 = (p1 + random.randint(1, HIJOS-2))%HIJOS
			pajaros[POBLACION - random.randint(1, HIJOS-1)].hijo(pajaros[p1], pajaros[p2])


		"""
		for i in range( int(HIJOS/2) ):
			pajaros[POBLACION-1 - i  ].hijo(pajaros[i], pajaros[i+1])
			pajaros[POBLACION-1 - i-1].hijo(pajaros[i], pajaros[i+1])
		"""

		# Mutacion
		for i in range(POBLACION):
			if i > HIJOS:
				if random.uniform(0, 1) <= MUTACIONCONEXION:
					pajaros[i].mutarConexion()

				if random.uniform(0, 1) <= MUTACIONCAMINO:			
					pajaros[i].mutarCamino()	

				if random.uniform(0, 1) <= MUTACIONACEPTACION:			
					pajaros[i].mutarActivacion()
				
				if random.uniform(0, 1) <= MUTACIONBIAS:			
					pajaros[i].mutarBias()

			pajaros[i].guardar("pesos/peso" + str(genPajaro))
			genPajaro += 1


algGenetico()