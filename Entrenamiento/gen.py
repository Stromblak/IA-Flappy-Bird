from flappy_gen import *
from red import ENTRADA, CAPA
import random
import os
import operator

POBLACION = 50
MUTACION = 5
DELTA = 0.1
MINFITNESS = 2500
HIJOS = 2
USARPESOS = True


class Pajaro:
	def __init__(self, archivo):
		self.fitness = 0

		if archivo == " ":
			self.pesos1 = [ [ 0 for i in range(ENTRADA)] for j in range(CAPA) ]
			self.pesos2 = [ 0 for i in range(CAPA) ]
			self.sal = random.randint(1, 10)

		else:
			self.pesos1 = np.loadtxt(archivo, dtype=float, max_rows=CAPA)
			self.pesos2 = np.loadtxt(archivo, dtype=float, skiprows=CAPA, max_rows=1)
			self.sal = np.loadtxt(archivo, dtype=float, skiprows=CAPA + 1)

	def nuevo(self, p1, p2):
		for i in range(CAPA):
			for j in range(ENTRADA):
				self.pesos1[i][j] = random.choice( [p1.pesos1[i][j], p2.pesos1[i][j]] )
	
		for i in range(CAPA):
			self.pesos2[i] = random.choice( [p1.pesos2[i], p2.pesos2[i]] )

		self.sal = random.choice( [p1.sal, p2.sal] )

		self.mutar()

	def donacion(self, don):
		for i in range(CAPA):
			for j in range(ENTRADA):
				self.pesos1[i][j] = random.choice( [self.pesos1[i][j], don.pesos1[i][j]] )
	
		for i in range(CAPA):
			self.pesos2[i] = random.choice( [self.pesos2[i], don.pesos2[i]] )

		self.sal = random.choice( [self.sal, don.sal] )

		self.mutar()

	def mutar(self):
		entrada = random.randint(0, ENTRADA-1)
		capa = random.randint(0, CAPA-1)

		delta = random.choice( [-DELTA, DELTA] )
		if delta > 0:
			self.pesos1[capa][entrada] = min(1, self.pesos1[capa][entrada] + delta)
			self.pesos2[capa] = min(1, self.pesos2[capa] + delta)
		
		else:
			self.pesos1[capa][entrada] = max(0, self.pesos1[capa][entrada] + delta)
			self.pesos2[capa] = max(0, self.pesos2[capa] + delta)
		
		self.sal = max(1, self.sal + 10*random.choice( [-DELTA, DELTA] ))
		# self.sal = min(5, self.sal)
		
	def guardar(self, archivo):
		if self.fitness < MINFITNESS:
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
			pajaros[POBLACION-1 - i  ].nuevo(pajaros[i], pajaros[i+1])
			pajaros[POBLACION-1 - i-1].nuevo(pajaros[i], pajaros[i+1])		

		# Mutacion y guardado de pesos
		for i in range(POBLACION):
			if MUTACION < random.randint(0, 100):
				pajaros[i].mutar()

			pajaros[i].guardar("pesos/peso" + str(genPajaro))
			genPajaro += 1


algGenetico()