import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


instancia = "calidad_neat_mov.txt"

f = open(instancia,'r')

maxRows = 800
nRow = 0

promedio, mejor = [], []
for row in f:
	row = row.split(' ')
	promedio.append(float(row[0]))
	mejor.append(float(row[1]))

	nRow += 1
	if nRow == maxRows:
		break

gen = [ i for i in range(len(promedio))]


windowSize = 20
polyOrder = 1

promedio = [ max(i, 0) for i in savgol_filter(promedio, windowSize, polyOrder) ]
mejor = [ max(i, 0) for i in savgol_filter(mejor, windowSize, polyOrder) ]

promedio[0] = 0
mejor[0] = 1

plt.subplots_adjust(bottom=0.3)

plt.plot(gen, promedio, label='Promedio')
plt.plot(gen, mejor, label='Mejor')

plt.xlabel("Generación")
plt.ylabel("Puntaje")
plt.title("Flappy Bird con tuberias moviendose")
plt.legend()
plt.show()