import numpy as np

ENTRADA = 8
CAPA1 = 4
CAPA2 = 4
PESOS1 = np.loadtxt("pesos.txt", dtype=float, max_rows=CAPA1)
PESOS2 = np.loadtxt("pesos.txt", dtype=float, skiprows=CAPA1, max_rows=CAPA2)
PESOS3 = np.loadtxt("pesos.txt", dtype=float, skiprows=CAPA1+CAPA2)

def red(tuberias, y, velCaida):
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
		capa1[i] = np.dot(entrada, PESOS1[i])
	
	for i in range(CAPA2):
		capa2[i] = np.dot(capa1, PESOS2[i])

	salida = np.dot(capa2, PESOS3)

	if salida > 1:
		return True
	else:
		return False





