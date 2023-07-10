import numpy as np

BIAS  = [1, 1, 0]
NODOS = [4 + BIAS[0], 4 + BIAS[1], 1]
CAPAS = len(NODOS)

def sig(x):
	return 1.0/(1 + np.exp(-x))

def procesarEntrada(tuberias, player):
	entrada = [player["velY"] / 10.0]

	for uPipe, lPipe in tuberias["tuberias"]:
		if uPipe["x"] + tuberias["w"] <= player["x"]:
			continue

		delta_Abajo  = (lPipe["y"]                           - player["y"] + player["h"]) / (322.0 - player["h"])
		delta_Final  = (min(148, uPipe["x"]) + tuberias["w"] - player["x"]              ) / (148.0)

		entrada.append( delta_Abajo )
		entrada.append( delta_Final )
		entrada.append( tuberias["delta"] )
		break

	if BIAS[0]:
		entrada.insert(0, 1)

	return np.array(entrada)


def red(tuberias, player, paj):
	# creacion red
	capas = [procesarEntrada(tuberias, player)]
	for i in range(1, CAPAS):
		capas.append( np.zeros(NODOS[i], dtype=float) )
		capas[-1][0] = 1


	# calculo red
	for i in range(1, CAPAS):
		for j in range(BIAS[i], NODOS[i]):
			if i != CAPAS-1:
				capas[i][j] = sig( np.dot(paj.pesos[i][j], capas[i-1]) )
			else:
				capas[i][j] = (np.dot(paj.pesos[i][j], capas[i-1]) >= 1)

	# Salida
	return capas[-1][-1]
	