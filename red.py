import numpy as np
import math

ARCHIVO = "pesos.txt"
NODOS = np.loadtxt(ARCHIVO, dtype=int, max_rows=1)
CAPAS = len(NODOS)

def cargarPesos():
	skip = 1
	pesos = [ [] ]
	for i in range(1, CAPAS):
		pesos.append( np.loadtxt(ARCHIVO, dtype=float, skiprows=skip, max_rows=NODOS[i]) )

		if pesos[-1].ndim == 1:
			pesos[-1] = [np.loadtxt(ARCHIVO, dtype=float, skiprows=skip, max_rows=NODOS[i])]
		skip += NODOS[i]

	pesos.append(np.loadtxt(ARCHIVO, dtype=float, skiprows=skip, max_rows=1))
	
	return pesos

def cargarEntrada(tuberias, player):
	entrada = [player["velY"]]

	# siguiente tuberia
	for uPipe, lPipe in tuberias["tuberias"]:
		if uPipe["x"] + tuberias["w"] <= player["x"]:
			continue

		distTubArriba = (uPipe["y"] + tuberias["h"]) - player["y"]
		distTubAbajo  = (lPipe["y"] - (player["y"] + player["h"]))
		distTubFinal  = (( min(150, uPipe["x"]) + tuberias["w"]) - player["x"])

		entrada.extend( [distTubArriba, distTubAbajo, distTubFinal] )
		break


	if len(entrada) != NODOS[0]:
		entrada.extend( [0 for i in range(NODOS[0] - len(entrada))] )

	return np.array(entrada)

PESOS = cargarPesos()

def red(tuberias, player):
	# creacion red
	capas = [cargarEntrada(tuberias, player)]
	for i in range(1, CAPAS):
		capas.append( np.zeros(NODOS[i], dtype=float) )
	
	# calculo red
	for i in range(1, CAPAS):
		for j in range(NODOS[i]):
			capas[i][j] = np.dot(PESOS[i][j], capas[i-1])

	# Salida
	
	if capas[-1][-1] >= PESOS[-1]:
		return True
	else:
		return False