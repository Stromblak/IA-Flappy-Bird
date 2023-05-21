from flappy_gen import *
from red import CAPA1, CAPA2, ENTRADA

main2()

class Pajaro:
	def __init__(self):
		self.pesos1 = [ [ random.uniform(0, 1) for i in range(ENTRADA)] for j in range(CAPA1) ]
		self.pesos2 = [ [ random.uniform(0, 1) for i in range(CAPA1)] for j in range(CAPA2) ]
		self.pesos3 = [ random.uniform(0, 1) for i in range(CAPA2) ]
		self.fitness = 0


while True:
	p = Pajaro()

	print(p.pesos1)

	crashInfo = mainGame(p.pesos1, p.pesos2, p.pesos3)
	print(crashInfo['score'])
	break


