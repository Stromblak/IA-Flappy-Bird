import numpy as np

ENTRADA = 5
CAPA1 = 4
CAPA2 = 4

def red(tuberias, x, y, velCaida, pesos1, pesos2, pesos3, sal):
	entrada = [y, velCaida]

	# x, y-arriba, y-abajo
	for uPipe, lPipe in tuberias:
		if uPipe["x"] < 50:
			continue
		entrada.extend( [uPipe["x"], uPipe["y"], lPipe["y"]] )
		break

	entrada = np.array(entrada)
	capa1 = np.zeros(CAPA1, dtype=float)
	capa2 = np.zeros(CAPA2, dtype=float)

	for i in range(CAPA1):
		capa1[i] = np.dot(entrada, pesos1[i])
	
	for i in range(CAPA2):
		capa2[i] = np.dot(capa1, pesos2[i])

	salida = np.dot(capa1, pesos3)
	# print(salida)
	
	if salida > sal:
		return True
	else:
		return False





