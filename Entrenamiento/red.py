import numpy as np
import math

NODOS = [3, 4, 3, 2, 1]
CAPAS = len(NODOS)

def red(tuberias, player, paj):
	entrada = [max(0, player["velY"])]

	# siguiente tuberia
	for uPipe, lPipe in tuberias["tuberias"]:
		if uPipe["x"] + tuberias["w"] <= player["x"]:
			continue

		distTubArriba = (uPipe["y"] + tuberias["h"] + tuberias["w"]) - player["y"]
		distTubAbajo  = (player["y"] + player["h"]) - (lPipe["y"] + tuberias["w"])

		entrada.extend( [ max(0, distTubArriba), max(0, distTubAbajo)] )
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
			capas[i][j] = np.dot(paj.pesos[i][j], capas[i-1])

	# Salida
	if capas[-1][-1] >= 1:
		return True
	else:
		return False