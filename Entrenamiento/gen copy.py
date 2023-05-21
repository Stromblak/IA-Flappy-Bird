from flappy_gen import *
from red import CAPA1, CAPA2, ENTRADA
from random import *

POBLACION = 10
MUTACION = 2

main2()

class Pajaro:
	def __init__(self):
		self.pesos1 = [ [ uniform(0, 1) for i in range(ENTRADA)] for j in range(CAPA1) ]
		self.pesos2 = [ [ uniform(0, 1) for i in range(CAPA1)] for j in range(CAPA2) ]
		self.pesos3 = [ uniform(0, 1) for i in range(CAPA2) ]
		self.fitness = 0
	
	def nuevo(self, p1, p2):
		for i in range(CAPA1):
			for j in range(ENTRADA):
				if randint(0, 1):
					self.pesos1[i][j] = p1.pesos1[i][j]
				else:
					self.pesos1[i][j] = p2.pesos1[i][j]

				if MUTACION > randint(0, 100):
					self.pesos1[i][j] = uniform(0, 1) 


		for i in range(CAPA2):
			for j in range(CAPA1):
				if randint(0, 1):
					self.pesos2[i][j] = p1.pesos2[i][j]
				else:
					self.pesos2[i][j] = p2.pesos2[i][j]

				if MUTACION > randint(0, 100):
					self.pesos2[i][j] = uniform(0, 1) 
	
		for i in range(CAPA2):
			if randint(0, 1):
				self.pesos3[i] = p1.pesos3[i]
			else:
				self.pesos3[i] = p2.pesos3[i]

			if MUTACION > randint(0, 100):
				if randint(0, 1):
					self.pesos3[i] = uniform(0, 1)

	def guardar(self, archivo):
		if self.fitness == 0:
			return
				
		f = open(archivo + "-" + str(self.fitness) + ".txt", 'w')

		for i in range(CAPA1):
			for j in range(ENTRADA):
				f.write( str(self.pesos1[i][j]) + " " )
			f.write("\n")


		for i in range(CAPA2):
			for j in range(CAPA1):
				f.write( str(self.pesos2[i][j]) + " " )
			f.write("\n")

		for i in range(CAPA2):
			f.write( str(self.pesos3[i]) + " " )
		
		f.close()


nPajaros = 0

while True:
	pajaros = [ Pajaro() for i in range(POBLACION) ]

	pesos1 = [pajaros[i].pesos1 for i in range(POBLACION)]
	pesos2 = [pajaros[i].pesos2 for i in range(POBLACION)]
	pesos3 = [pajaros[i].pesos3 for i in range(POBLACION)]

	crashInfo = mainGame(POBLACION, pesos1, pesos2, pesos3)

	for i in range(POBLACION):
		pajaros[i].fitness = crashInfo[i]

	p = sample(range(POBLACION), 4)
	if pajaros[p[0]].fitness > pajaros[p[1]].fitness:
		p1 = p[0]
		h1 = p[1]
	else:
		p1 = p[1]
		h1 = p[0]

	if pajaros[p[2]].fitness > pajaros[p[3]].fitness:
		p2 = p[2]
		h2 = p[3]
	else:
		p2 = p[2]
		h2 = p[3]

	pajaros[h1].nuevo(pajaros[p1], pajaros[p2])
	pajaros[h2].nuevo(pajaros[p1], pajaros[p2])

	for i in range(POBLACION):
		pajaros[i].guardar("pesos/peso" + str(nPajaros))
		nPajaros += 1


