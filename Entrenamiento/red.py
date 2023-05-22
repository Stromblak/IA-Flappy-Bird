import numpy as np
import math
import random

ENTRADA = 3
CAPA = 3

def red(tuberias, x, y, vely, pesos1, pesos2, sal):
	entrada = [ abs(vely) ]

	# siguiente tuberia
	for uPipe, lPipe in tuberias:
		if uPipe["x"] <= x - 30:
			continue
		# entrada.extend( [-uPipe["x"], uPipe["y"], lPipe["y"]] )
		tubArriba = [uPipe["x"], uPipe["y"]]
		tubAbajo  = [lPipe["x"], lPipe["y"]]
		pajaro    = [x, y]

		entrada.extend( [math.dist(pajaro, tubArriba), math.dist(pajaro, tubAbajo)] )
		break

	entrada = np.array(entrada)
	capa = np.zeros(CAPA, dtype=float)

	for i in range(CAPA):
		capa[i] = np.dot(entrada, pesos1[i])
	
	salida = np.dot(capa, pesos2)

	if not random.randint(1, 100):
		print(salida)
	
	if salida > sal:
		return True
	else:
		return False