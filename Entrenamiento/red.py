import numpy as np
import math

NODOS = [7, 3, 1]
CAPAS = len(NODOS)
MODO = 3

def red(tuberias, player, paj):
	entrada = [player["velY"]]

	# siguiente tuberia
	
	for uPipe, lPipe in tuberias["tuberias"]:
		if uPipe["x"] + tuberias["w"] <= player["x"]:
			continue
		
		if MODO == 1:
			distTubArriba = (uPipe["y"] + tuberias["h"]) - player["y"]
			distTubAbajo  = lPipe["y"] - (player["y"] + player["h"])
			entrada.extend( [distTubArriba, distTubAbajo] )

		elif MODO == 2:
			tubArriba = [uPipe["x"] + tuberias["w"], uPipe["y"] + tuberias["h"]]
			tubAbajo  = [lPipe["x"] + tuberias["w"], lPipe["y"]]
			pajaroArriba = [player["x"], player["y"]]
			pajaroAbajo  = [player["x"], player["y"] + player["h"]]
			entrada.extend( [math.dist(pajaroArriba, tubArriba), math.dist(pajaroAbajo, tubAbajo)] )

		elif MODO == 3:
			input = [player["y"], player["h"], uPipe["y"] + tuberias["h"], lPipe["y"], uPipe["x"], tuberias["w"]]
			entrada.extend(input)
		break

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