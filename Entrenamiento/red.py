import numpy as np
import math
import random


NODOS = [3 + 1, 3 + 1, 1]
CAPAS = len(NODOS)

def sigmoid(w):
	return w
	#return 1/(1 + np.exp(-w + b))

def procesarEntrada(tuberias, player):
	entrada = [player["velY"]]

	# siguiente tuberia
	for uPipe, lPipe in tuberias["tuberias"]:
		if uPipe["x"] + tuberias["w"] <= player["x"]:
			continue

		distTubArriba = (uPipe["y"] + tuberias["h"] - player["y"])
		distTubAbajo  = (lPipe["y"] - (player["y"] + player["h"]))		
		distTubFinal  = (( min(150, uPipe["x"]) + tuberias["w"]) - player["x"])
		entrada.extend( [distTubArriba, distTubAbajo] )
		
		break


	if len(entrada) != NODOS[0]:
		entrada.extend( [0 for i in range(NODOS[0] - len(entrada))] )

	return np.array(entrada)


def red(tuberias, player, paj):
	# creacion red
	capas = [procesarEntrada(tuberias, player)]
	for i in range(1, CAPAS):
		capas.append( np.zeros(NODOS[i], dtype=float) )
		capas[-1][0] = 1

	# calculo red
	for i in range(1, CAPAS):
		for j in range(NODOS[i]):
			capas[i][j] = sigmoid( np.dot(paj.pesos[i][j], capas[i-1]) )

	# Salida	
	if capas[-1][-1] >= paj.pesos[-1]:
		return True
	
	return False