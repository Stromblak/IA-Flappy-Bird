import matplotlib.pyplot as plt


instancia = "calidad_gen.txt"

f = open(instancia,'r')

maxRows = 500
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

plt.plot(gen, promedio, label= 'Promedio')
plt.plot(gen, mejor, label= 'Mejor')

plt.title("inst")
plt.show()