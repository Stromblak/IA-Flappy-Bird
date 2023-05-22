import numpy as np
import math

ENTRADA = 3
CAPA = 3
PESOS1 = np.loadtxt("pesos.txt", dtype=float, max_rows=CAPA)
PESOS2 = np.loadtxt("pesos.txt", dtype=float, skiprows=CAPA, max_rows=1)
SALIDA = np.loadtxt("pesos.txt", dtype=float, skiprows=CAPA + 1)

def red(tuberias, x, y, vely):
	entrada = [vely]

	# siguiente tuberia
	for uPipe, lPipe in tuberias:
		if uPipe["x"] <= x - 30:
			continue
		tubArriba = [uPipe["x"], uPipe["y"]]
		tubAbajo  = [lPipe["x"], lPipe["y"]]
		pajaro    = [x, y]

		entrada.append( math.dist(pajaro, tubArriba) )
		entrada.append( math.dist(pajaro, tubAbajo) )
		break

	entrada = np.array(entrada)
	capa = np.zeros(CAPA, dtype=float)

	# Primera capa
	for i in range(CAPA):
		capa[i] = np.dot(entrada, PESOS1[i])
	
	# Valor salida
	salida = np.dot(capa, PESOS2)

	# Salida
	if salida > SALIDA:
		return True
	else:
		return False