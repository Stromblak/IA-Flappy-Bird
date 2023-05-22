import numpy as np
import math

ENTRADA = 3
CAPA = 3

def red(tuberias, x, y, vely, paj):
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
		capa[i] = np.dot(entrada, paj.pesos1[i])
	
	# Valor salida
	salida = np.dot(capa, paj.pesos2)

	# Salida
	if salida > paj.sal:
		return True
	else:
		return False