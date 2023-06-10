from flappy_gen import *
from red import NODOS, CAPAS
import random
import os
import operator
import statistics

POBLACION = 1000

# 			camino conexion activacion bias
MUTACION 	= [0.0, 	0.3, 	0.1, 	0.2]
DELTA 		= [0.0, 	0.1, 	0.1, 	0.05]

MINFITNESS = 3000
HIJOS = int(POBLACION*0.1)
WMIN, WMAX = -1, 1

RANDOM = True
USARPESOS = False

class Pajaro:
	def __init__(self):
		self.fitness = 0

		self.pesos = [ [] ]
		for i in range(1, CAPAS):
			self.pesos.append( [] )

			for j in range(NODOS[i]):
				self.pesos[i].append( np.zeros(NODOS[i-1], dtype=float) )

				if RANDOM:
					for k in range(NODOS[i-1]):
						self.pesos[i][-1][k] = random.uniform(WMIN, WMAX)

		self.pesos.append(0.5)

		self.bias = [ [] ]
		for i in range(1, CAPAS):
			self.bias.append( np.zeros(NODOS[i], dtype=float) )

	def hijo(self, p1, p2):
		if p1.fitness < 100 or p1.fitness < 100:
			return

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

		for i in range(1, CAPAS):
			nuevo = self.pesos[i][ camino[i] ][ camino[i-1] ] + random.uniform(-1, 1) * DELTA[0]
			self.pesos[i][ camino[i] ][ camino[i-1] ] = np.clip(nuevo, WMIN, WMAX)

	def mutarConexion(self):
		capa  = random.randint(1, CAPAS-1)
		nodoCapa = random.randint(0, NODOS[capa]-1)
		nodoAnterior = random.randint(0, NODOS[capa-1]-1)

		nuevo = self.pesos[capa][nodoCapa][nodoAnterior] + random.uniform(-1, 1) * DELTA[1]
		self.pesos[capa][nodoCapa][nodoAnterior] = np.clip(nuevo, WMIN, WMAX)
	
	def mutarActivacion(self):
		delta = random.uniform(-1, 1) * DELTA[2]	
		self.pesos[-1] = max(1, self.pesos[-1] + delta)

	def mutarBias(self):
		capa  = random.randint(1, CAPAS-1)
		nodoCapa = random.randint(0, NODOS[capa]-1)
		self.bias[capa][nodoCapa] += random.uniform(-1, 1) * DELTA[3]

	def guardar(self, archivo):
		if self.fitness < MINFITNESS:
			return
				
		f = open(archivo + "-" + str(self.fitness) + ".txt", 'w')

		f.write( " ".join( [str(v) for v in NODOS]) + "\n")
		for i in range(1, CAPAS):
			for j in range(NODOS[i]):
				f.write( " ".join( [str(v) for v in self.pesos[i][j]]) + "\n")

		f.write(str(self.pesos[-1]))
		f.close()	

	def cargar(self, archivo):
		skip = 1
		pesos = [ [] ]
		for i in range(1, CAPAS):
			pesos.append( np.loadtxt(archivo, dtype=float, skiprows=skip, max_rows=NODOS[i]) )

			if pesos[-1].ndim == 1:
				pesos[-1] = [np.loadtxt(archivo, dtype=float, skiprows=skip, max_rows=NODOS[i])]
			skip += NODOS[i]

		pesos.append(np.loadtxt(archivo, dtype=float, skiprows=skip, max_rows=1))
		
		self.pesos = pesos


def algGenetico():
	main2()
	genPajaro = 0

	# Creacion poblacion
	if USARPESOS:
		dir_list = os.listdir("./pesos")
		pajaros = [ Pajaro( "./pesos/" + dir_list[i] ) for i in range(len(dir_list)) ]
		pajaros.extend( [ Pajaro(" ") for i in range(len(dir_list), POBLACION) ])
	
	else:
		pajaros = [ Pajaro() for i in range(POBLACION) ]


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
				if random.uniform(0, 1) <= MUTACION[0]:			
					pajaros[i].mutarCamino()	

				if random.uniform(0, 1) <= MUTACION[1]:
					pajaros[i].mutarConexion()

				if random.uniform(0, 1) <= MUTACION[2]:			
					pajaros[i].mutarActivacion()
				
				if random.uniform(0, 1) <= MUTACION[3]:			
					pajaros[i].mutarBias()

			pajaros[i].guardar("pesos/peso" + str(genPajaro))
			genPajaro += 1


algGenetico()