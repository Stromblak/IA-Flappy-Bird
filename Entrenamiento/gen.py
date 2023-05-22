from flappy_gen import *
from red import CAPA1, CAPA2, ENTRADA
from random import *

POBLACION = 20
MUTACION = 1
DELTA = 0.05

main2()

class Pajaro:
	def __init__(self):
		self.pesos1 = [ [ uniform(0, 1) for i in range(ENTRADA)] for j in range(CAPA1) ]
		self.pesos2 = [ [ uniform(0, 1) for i in range(CAPA1)] for j in range(CAPA2) ]
		self.pesos3 = [ uniform(0, 1) for i in range(CAPA2) ]
		self.fitness = 0
		self.sal = randint(500, 2000)
	
	def nuevo(self, p1, p2):
		for i in range(CAPA1):
			for j in range(ENTRADA):
				if randint(0, 1):
					self.pesos1[i][j] = p1.pesos1[i][j]
				else:
					self.pesos1[i][j] = p2.pesos1[i][j]

		for i in range(CAPA2):
			for j in range(CAPA1):
				if randint(0, 1):
					self.pesos2[i][j] = p1.pesos2[i][j]
				else:
					self.pesos2[i][j] = p2.pesos2[i][j]
	
		for i in range(CAPA2):
			if randint(0, 1):
				self.pesos3[i] = p1.pesos3[i]
			else:
				self.pesos3[i] = p2.pesos3[i]

		if randint(0, 1):
			self.sal = p1.sal
		else:
			self.sal = p2.sal

		self.mutar()

	def mutar(self):
		for i in range(CAPA1):
			for j in range(ENTRADA):
				if MUTACION > randint(0, 100):
					self.pesos1[i][j] = uniform(0, 1) #= uniform(-DELTA, DELTA)


		for i in range(CAPA2):
			for j in range(CAPA1):
				if MUTACION > randint(0, 100):
					self.pesos2[i][j] = uniform(0, 1) # += uniform(-DELTA, DELTA)
	
		for i in range(CAPA2):
			if MUTACION > randint(0, 100):
				self.pesos3[i] = uniform(0, 1) # += uniform(-DELTA, DELTA)

		if MUTACION > randint(0, 100):
			self.sal = uniform(100, 2000) # += uniform(-DELTA*1000, DELTA*1000)

	def guardar(self, archivo):
		if self.fitness < 200:
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
		f.write("\n")	
		f.write(str(self.sal))

		f.close()


nPajaros = 0

while True:
	pajaros = [ Pajaro() for i in range(POBLACION) ]

	pesos1 = [pajaros[i].pesos1 for i in range(POBLACION)]
	pesos2 = [pajaros[i].pesos2 for i in range(POBLACION)]
	pesos3 = [pajaros[i].pesos3 for i in range(POBLACION)]
	sal = [pajaros[i].sal for i in range(POBLACION)]


	crashInfo = mainGame(POBLACION, pesos1, pesos2, pesos3, sal)

	# resultado
	for i in range(POBLACION):
		pajaros[i].fitness = crashInfo[i]

	# descendencia
	max, max2 = -1, -1
	min, min2 = 10000, 10000
	for i in range(POBLACION):
		if pajaros[i].fitness > max:
			max2 = max
			max = i

		if max2 < pajaros[i].fitness < max:
			max2 = i

		if pajaros[i].fitness < min:
			min2 = min
			min = i

		if min2 > pajaros[i].fitness > min:
			min2 = i

	pajaros[min].nuevo(pajaros[max], pajaros[max2])
	pajaros[min2].nuevo(pajaros[max], pajaros[max2])

	for i in range(POBLACION):
		if MUTACION > randint(0, 100):
			pajaros[i].mutar()
		pajaros[i].guardar("pesos/peso" + str(nPajaros))
		nPajaros += 1


