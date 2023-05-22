from flappy_gen import *
from red import ENTRADA, CAPA
from random import *

POBLACION = 100
MUTACION = 10
DELTA = 0.05


class Pajaro:
	def __init__(self):
		self.pesos1 = [ [ 0 for i in range(ENTRADA)] for j in range(CAPA) ]
		self.pesos2 = [ 0 for i in range(CAPA) ]
		self.fitness = 0
		self.sal = 1 # uniform(100, 2000)
	
	def nuevo(self, p1, p2):
		for i in range(CAPA):
			for j in range(ENTRADA):
				self.pesos1[i][j] = choice( [p1.pesos1[i][j], p2.pesos1[i][j]] )
	
		for i in range(CAPA):
			self.pesos2[i] = choice( [p1.pesos2[i], p2.pesos2[i]] )

		self.sal = choice( [p1.sal, p2.sal] )

		self.mutar()

	def mutar(self):
		entrada = randint(0, ENTRADA-1)
		capa = randint(0, CAPA-1)

		delta = choice( [DELTA, -DELTA] )
		if delta > 0:
			self.pesos1[capa][entrada] = min(1, self.pesos1[capa][entrada] + delta)
			self.pesos2[capa] = min(1, self.pesos2[capa] + delta)
		
		else:
			self.pesos1[capa][entrada] = max(0, self.pesos1[capa][entrada] + delta)
			self.pesos2[capa] = max(0, self.pesos2[capa] + delta)
		
		self.sal = max(1, self.sal + choice( [DELTA, -DELTA] )*20)

	def guardar(self, archivo):
		if self.fitness < 200:
			return
				
		f = open(archivo + "-" + str(self.fitness) + ".txt", 'w')

		for i in range(CAPA):
			for j in range(ENTRADA):
				f.write( str(self.pesos1[i][j]) + " " )
			f.write("\n")

		for i in range(CAPA):
			f.write( str(self.pesos2[i]) + " " )
		f.write("\n")	
		f.write(str(self.sal))

		f.close()


main2()
genPajaro = 0
maxAnterior = -1
pajaros = [ Pajaro() for i in range(POBLACION) ]

while True:
	pesos1 = [pajaros[i].pesos1 for i in range(POBLACION)]
	pesos2 = [pajaros[i].pesos2 for i in range(POBLACION)]
	sal = [pajaros[i].sal for i in range(POBLACION)]


	crashInfo = mainGame(POBLACION, pesos1, pesos2, sal)

	# resultado
	for i in range(POBLACION):
		pajaros[i].fitness = crashInfo[i]

	# descendencia
	max1, max2 = -1, -1
	min1, min2 = 10000, 10000
	for i in range(POBLACION):
		if pajaros[i].fitness > max1:
			max2 = max1
			max1 = i

		if max2 < pajaros[i].fitness < max1:
			max2 = i

		if pajaros[i].fitness < min1:
			min2 = min1
			min1 = i

		if min2 > pajaros[i].fitness > min1:
			min2 = i

	pajaros[min1].nuevo(pajaros[max1], pajaros[max2])
	pajaros[min2].nuevo(pajaros[max1], pajaros[max2])

	for i in range(POBLACION):
		if MUTACION < randint(0, 100) and i != max1 and i != maxAnterior:
			pajaros[i].mutar()

		pajaros[i].guardar("pesos/peso" + str(genPajaro))
		genPajaro += 1
	
	maxAnterior = max1


