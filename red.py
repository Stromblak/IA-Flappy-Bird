import numpy as np
import math
import random

ENTRADA = 3
CAPA = 3
PESOS1 = np.loadtxt("pesos.txt", dtype=float, max_rows=CAPA)
PESOS2 = np.loadtxt("pesos.txt", dtype=float, skiprows=CAPA, max_rows=1)
SALIDA = np.loadtxt("pesos.txt", dtype=float, skiprows=CAPA + 1)

def red(tuberias, x, y, vely):
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
		capa[i] = np.dot(entrada, PESOS1[i])
	
	salida = np.dot(capa, PESOS2)

	if not random.randint(1, 100):
		print(salida)
	
	if salida > SALIDA:
		return True
	else:
		return False