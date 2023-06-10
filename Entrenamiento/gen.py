from flappy_gen import *
from red import NODOS, CAPAS
import random
import os
import operator
import statistics
import  matplotlib.pyplot as plt

POBLACION = 100
HIJOS = int(POBLACION*0.1)

# 			  camino 	peso activacion bias
MUTACION 	= [0.0, 	0.1, 	0.0, 	0.1]
DELTA 		= [0.0,		0.01, 	0.0, 	0.01]
WMIN, WMAX = -1, 1
WACTIVACION = 1

RANDOM = True
USARPESOS = False
MINFITNESS = 3000

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

		self.pesos.append(WACTIVACION)

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
		self.mutarPeso()
		self.mutarBias()

		self.fitness = p1.fitness + p2.fitness

	def mutarCamino(self):
		camino = []
		for i in range(CAPAS):
			camino.append( random.randint(0, NODOS[i]-1) )

		for i in range(1, CAPAS):
			nuevo = self.pesos[i][ camino[i] ][ camino[i-1] ] + random.uniform(-1, 1) * DELTA[0]
			self.pesos[i][ camino[i] ][ camino[i-1] ] = np.clip(nuevo, WMIN, WMAX)

	def mutarPeso(self):
		for i in range(1, CAPAS):
			for j in range(NODOS[i]):
				for k in range(NODOS[i-1]):
					if random.uniform(0, 1) <= MUTACION[1]:
						nuevo = self.pesos[i][j][k] + random.uniform(-1, 1) * DELTA[1]
						self.pesos[i][j][k] = np.clip(nuevo, WMIN, WMAX)

		return
		capa  = random.randint(1, CAPAS-1)
		nodoCapa = random.randint(0, NODOS[capa]-1)
		nodoAnterior = random.randint(0, NODOS[capa-1]-1)

		nuevo = self.pesos[capa][nodoCapa][nodoAnterior] + random.uniform(-1, 1) * DELTA[1]
		self.pesos[capa][nodoCapa][nodoAnterior] = np.clip(nuevo, WMIN, WMAX)
	
	def mutarActivacion(self):
		delta = random.uniform(-1, 1) * DELTA[2]	
		self.pesos[-1] += delta
		#self.pesos[-1] = max(1, self.pesos[-1] + delta)

	def mutarBias(self):
		capa  = random.randint(1, CAPAS-1)
		nodoCapa = random.randint(0, NODOS[capa]-1)
		self.bias[capa][nodoCapa] += random.uniform(-1, 1) * DELTA[3]

	def guardar(self, archivo):
		if self.fitness < MINFITNESS:
			return

		f = open(archivo + "-" + str(self.fitness) + ".txt", 'w')

		f.write( " ".join( [str(n) for n in NODOS]) + "\n")
		for i in range(1, CAPAS):
			for j in range(NODOS[i]):
				f.write( " ".join( [str(p) for p in self.pesos[i][j]]) + "\n")

		f.write(str(self.pesos[-1]))

		for i in range(1, CAPAS):
			f.write( " ".join( [str(b) for b in self.bias[i]]) + "\n")

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


class AlgGenetico():
	def __init__(self):
		main2()
		self.numPajaro = 0
		self.pajaros = [ Pajaro() for i in range(POBLACION) ]
		if USARPESOS:
			dir_list = os.listdir("./pesos")
			for i in range(min(len(dir_list), POBLACION)):
				self.pajaros[i].cargar("./pesos/" + dir_list[i])
		
		self.fitnessMaxGen = []
		self.fitnessPromedioGen = []

	def ciclo(self):
		self.calculoFitness()
		self.descendencia()
		self.mutacion()

	def calculoFitness(self):
		fitness = mainGame(POBLACION, self.pajaros)
		
		for i in range(POBLACION):
			self.pajaros[i].fitness = fitness[i] #(pajaros[i].fitness + fitness[i])/2
			self.pajaros[i].guardar("pesos/peso" + str(self.numPajaro))		
			self.numPajaro += 1

		# [mejor fitness, ..., peor fitness]
		self.pajaros.sort(reverse=True, key=operator.attrgetter('fitness'))
		# print([p.fitness for p in self.pajaros])

		self.fitnessMaxGen.append(self.pajaros[0].fitness)
		self.fitnessPromedioGen.append(statistics.mean(fitness))
		print(self.fitnessPromedioGen[-1], self.fitnessMaxGen[-1])

	def descendencia(self):
		self.pajaros[-1].hijo(self.pajaros[0], self.pajaros[0])
		for i in range(HIJOS):
			p1 = random.randint(0, HIJOS-1)
			p2 = (p1 + random.randint(1, HIJOS-2))%HIJOS
			self.pajaros[POBLACION-2 - i].hijo(self.pajaros[p1], self.pajaros[p2])

		"""
		for i in range( int(HIJOS/2) ):
			pajaros[POBLACION-1 - i  ].hijo(pajaros[i], pajaros[i+1])
			pajaros[POBLACION-1 - i-1].hijo(pajaros[i], pajaros[i+1])
		"""		

	def mutacion(self):
		for i in range(POBLACION):
			if i > HIJOS:
				if MUTACION[0] <= random.uniform(0, 1):			
					self.pajaros[i].mutarCamino()	

				if MUTACION[1] <= random.uniform(0, 1):
					self.pajaros[i].mutarPeso()

				if MUTACION[2] <= random.uniform(0, 1):			
					self.pajaros[i].mutarActivacion()
				
				if MUTACION[3] <= random.uniform(0, 1):			
					self.pajaros[i].mutarBias()		

	def grafico(self):
		x = [i for i in range(len(self.fitnessMaxGen))]
		plt.plot(x, self.fitnessMaxGen, label = "Mejor")
		plt.plot(x, self.fitnessPromedioGen, label = "Promedio")

		plt.xlabel('Generacion')
		plt.ylabel('Fitness')

		plt.legend()
		plt.show()


instancia = AlgGenetico()
while True:
	try:
		instancia.ciclo()

	except KeyboardInterrupt:
		instancia.grafico()
		sys.exit()