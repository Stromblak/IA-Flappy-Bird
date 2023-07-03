import numpy as np

BIAS = [1, 1, 0]
NODOS = [4 + BIAS[0], 4 + BIAS[1], 1]
CAPAS = len(NODOS)

def sigmoid(w):
	return 1.0/(1 + np.exp(-w))

def procesarEntrada(tuberias, player):
	entrada = [player["velY"] / 10.0]

	siguiente = 0
	for uPipe, lPipe in tuberias["tuberias"]:
		if uPipe["x"] + tuberias["w"] <= player["x"]:
			continue

		diff_Arriba = (uPipe["y"] + tuberias["h"]           - player["y"]              ) / 260.0
		diff_Abajo  = (lPipe["y"]                           - player["y"] + player["h"]) / 262.48
		diff_Final  = (min(149, uPipe["x"]) + tuberias["w"] - player["x"]              ) / 149.0

		entrada.append( diff_Abajo )

		if not siguiente:
			entrada.append(diff_Final)
			siguiente = 1
			continue

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
				capas[i][j] = sigmoid( np.dot(paj.pesos[i][j], capas[i-1]) )
			else:
				capas[i][j] = (np.dot(paj.pesos[i][j], capas[i-1]) >= 1)

	# Salida
	return capas[-1][-1]
	