import numpy as np

ENTRADA = 8
CAPA1 = 4
CAPA2 = 4

def red(tuberias, y, velCaida, pesos1, pesos2, pesos3):
	entrada = [y, velCaida] 
	tubs = 0

	# x, y-arriba, y-abajo
	for uPipe, lPipe in tuberias:
		entrada.extend( [uPipe["x"], uPipe["y"], lPipe["y"]] )
		tubs += 1
		if tubs == 2:
			break

	entrada = np.array(entrada)
	capa1 = np.zeros(CAPA1, dtype=float)
	capa2 = np.zeros(CAPA2, dtype=float)

	for i in range(CAPA1):
		capa1[i] = np.dot(entrada, pesos1[i])
	
	for i in range(CAPA2):
		capa2[i] = np.dot(capa1, pesos2[i])

	salida = np.dot(capa2, pesos3)

	if salida > 1:
		return True
	else:
		return False





