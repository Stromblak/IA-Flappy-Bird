from flappy_gen import *
from red import NODOS, CAPAS, BIAS
import random
import os
import statistics
import matplotlib.pyplot as plt

POBLACION = 1000
HIJOS  = int(POBLACION * 0.2)
PADRES = int(POBLACION * 0.2)

MUTACION = 0.2
DELTA    = 0.02

WMIN, WMAX = -1, 1
RANDOM = True
USARPESOS = False
MINFITNESS = 6000

def prob(p):
	if random.uniform(0, 1) < p: return True
	else: return False


class Pajaro:
	def __init__(self):
		self.fitness = 0
		self.distMuerte = 0

		self.pesos = [ [] ]
		for i in range(1, CAPAS):
			self.pesos.append( [] )

			for j in range(NODOS[i]):
				self.pesos[i].append( np.zeros(NODOS[i-1], dtype=float) )

				if RANDOM:
					for k in range(NODOS[i-1]):
						self.pesos[i][-1][k] = random.uniform(WMIN, WMAX)

	def hijo(self, p1, p2):
		for i in range(1, CAPAS):
			for j in range(NODOS[i]):
				for k in range(NODOS[i-1]):
					self.pesos[i][j][k] = random.choice([p1.pesos[i][j][k], p2.pesos[i][j][k]])

		#self.pesos[-1] = random.choice([p1.pesos[-1], p2.pesos[-1]])

		self.mutar()

	def mutar(self):
		for i in range(1, CAPAS):
			for j in range(NODOS[i]):
				for k in range(NODOS[i-1]):
					if prob(MUTACION):
						self.pesos[i][j][k] += random.uniform(-1, 1) * DELTA
	
	def guardar(self, archivo):
		if self.fitness < MINFITNESS:
			return
		
		f = open(archivo + "-" + str(self.fitness) + ".txt", 'w')

		f.write( " ".join( [str(n) for n in BIAS]) + "\n")
		f.write( " ".join( [str(n) for n in NODOS]) + "\n")

		for i in range(1, CAPAS):
			for j in range(NODOS[i]):
				f.write( " ".join( [str(p) for p in self.pesos[i][j]]) + "\n")

		f.close()	


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

		self.f = open("calidad.txt", "w")

	def ciclo(self):
		self.calculoFitness()
		self.descendencia()
		self.mutacion()

	def calculoFitness(self):
		fitness, distPipe = mainGame(POBLACION, self.pajaros)
		
		for i in range(POBLACION):
			self.pajaros[i].fitness = fitness[i]
			self.pajaros[i].distMuerte = distPipe[i]
			self.pajaros[i].guardar("pesos/peso" + str(self.numPajaro))		
			self.numPajaro += 1
		
		# [mejor fitness, ..., peor fitness]
		self.pajaros.sort(key=lambda x: (-x.fitness, x.distMuerte))

		# print([ [p.fitness, p.distMuerte] for p in self.pajaros])


		self.fitnessMaxGen.append(self.pajaros[0].fitness)
		self.fitnessPromedioGen.append(statistics.mean(fitness))
		print(self.fitnessPromedioGen[-1], self.fitnessMaxGen[-1])

		self.f.write(str(self.fitnessPromedioGen[-1]) + " " + str(self.fitnessMaxGen[-1]) + "\n")

	def descendencia(self):
		for i in range(HIJOS):
			p1 = random.randint(0, 4) #random.randint(0, HIJOS-1)
			p2 = (p1 + random.randint(1, PADRES-1)) % PADRES
			self.pajaros[POBLACION-1 - i].hijo(self.pajaros[p1], self.pajaros[p2])

	def mutacion(self):
		for i in range(1, POBLACION):
			if prob(MUTACION):
				self.pajaros[i].mutar()

	def grafico(self):
		x = [i for i in range(len(self.fitnessMaxGen))]
		plt.plot(x, self.fitnessMaxGen, label = "Mejor")
		plt.plot(x, self.fitnessPromedioGen, label = "Promedio")

		plt.xlabel('Generacion')
		plt.ylabel('Fitness')

		plt.legend()
		plt.show()


# ---------------------
instancia = AlgGenetico()
while True:
	try:
		instancia.ciclo()

	except KeyboardInterrupt:
		instancia.grafico()
		sys.exit()