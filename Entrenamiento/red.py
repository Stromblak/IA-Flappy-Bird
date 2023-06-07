import numpy as np
import math

NODOS = [3, 4, 3, 2, 1]
CAPAS = len(NODOS)

def red(tuberias, x, y, vely, paj):
	entrada = [max(0, vely)]

	# siguiente tuberia
	for uPipe, lPipe in tuberias:
		if uPipe["x"] <= x - 30:
			continue

		entrada.extend( [ max(0, uPipe["y"] - y), max(0, y - lPipe["y"])] )
		break
	"""
	for uPipe, lPipe in tuberias:
		if uPipe["x"] <= x - 30:
			continue
		tubArriba = [uPipe["x"], uPipe["y"]]
		tubAbajo  = [lPipe["x"], lPipe["y"]]
		pajaro    = [x, y]

		entrada.append( math.dist(pajaro, tubArriba) )
		entrada.append( math.dist(pajaro, tubAbajo) )
		break
	"""

	if len(entrada) != NODOS[0]:
		entrada.extend( [0 for i in range(NODOS[0] - len(entrada))] )

	# creacion red
	capas = [np.array(entrada)]
	for i in range(1, CAPAS):
		capas.append( np.zeros(NODOS[i], dtype=float) )

	# calculo red
	for i in range(1, CAPAS):
		for j in range(NODOS[i]):
			capas[i][j] = np.dot(capas[i-1], paj.pesos[i-1][j])

	# Salida
	if capas[-1][0] >= 1:
		return True
	else:
		return False