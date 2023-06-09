import numpy as np
import math

NODOS = [2, 3, 1]
CAPAS = len(NODOS)

def sigmoid(w, b):
	return w
	return 1/(1 + np.exp(-w + b))

def red(tuberias, player, paj):
	entrada = [player["velY"]]

	# siguiente tuberia
	primera = 0
	for uPipe, lPipe in tuberias["tuberias"]:

		if 0 and uPipe["x"] + tuberias["w"] <= player["x"]:
			continue

		if uPipe["x"] <= player["x"] - 30:
			continue
		tubAbajo  = [min(200, lPipe["x"]), lPipe["y"]]
		pajaro = [player["x"], player["y"]]

		entrada.append( math.dist(pajaro, tubAbajo) )

		break

		pajaro = [player["x"] + player["w"]/2, player["y"] + player["h"]/2]
		tub = [uPipe["x"] + tuberias["w"]/2, (uPipe["y"] + tuberias["h"] + lPipe["y"])/2]

		if tub[0] > 100: tub[0] = 100
		entrada.extend( [math.dist(pajaro, tub)] )

		break
		distTubArriba = abs(uPipe["y"] + tuberias["h"]) - player["y"]
		distTubAbajo  = abs(lPipe["y"] - (player["y"] + player["h"]))
		entrada.extend( [distTubArriba, distTubAbajo] )

		break
		pajaro = [player["x"] + player["w"]/2, player["y"] + player["h"]/2]
		tubArriba = [uPipe["x"] + tuberias["w"]/2, uPipe["y"] + tuberias["h"]]
		tubAbajo  = [lPipe["x"] + tuberias["w"]/2, lPipe["y"]]
		entrada.extend( [math.dist(pajaro, tubArriba), math.dist(pajaro, tubAbajo)] )
		break

		distTubArriba = abs(uPipe["y"] + tuberias["h"]) - player["y"]
		distTubAbajo  = abs(lPipe["y"] - (player["y"] + player["h"]))
		# distFinal  = abs(player["x"] - (uPipe["x"] + tuberias["w"]))

		entrada.extend( [distTubArriba, distTubAbajo] )

		break

		tubArriba = [uPipe["x"] + tuberias["w"]/2, uPipe["y"] + tuberias["h"]]
		tubAbajo  = [lPipe["x"] + tuberias["w"]/2, lPipe["y"]]
		pajaroArriba = [player["x"], player["y"]]
		pajaroAbajo  = [player["x"], player["y"] + player["h"]]
		entrada.extend( [math.dist(pajaroArriba, tubArriba), math.dist(pajaroAbajo, tubAbajo)] )
		break
		if primera: break
		else: primera += 1
		"""

		tubArriba = [uPipe["x"] + tuberias["w"], uPipe["y"] + tuberias["h"]]
		tubAbajo  = [lPipe["x"] + tuberias["w"], lPipe["y"]]
		pajaroArriba = [player["x"], player["y"]]
		pajaroAbajo  = [player["x"], player["y"] + player["h"]]
		entrada.extend( [math.dist(pajaroArriba, tubArriba), math.dist(pajaroAbajo, tubAbajo)] )

		input = [player["y"], player["h"], uPipe["y"] + tuberias["h"], lPipe["y"], uPipe["x"], tuberias["w"]]
		entrada.extend(input)
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
			capas[i][j] = sigmoid( -np.dot(paj.pesos[i][j], capas[i-1]), paj.bias[i][j] )

	# Salida
	if capas[-1][-1] >= paj.pesos[-1]:
		return True
	else:
		return False