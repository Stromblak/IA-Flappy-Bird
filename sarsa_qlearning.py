import random
from flappy import *
import json

Q = {}  # Diccionario para almacenar Q's, guarda un par estado y accion (Q es el valor)
a = 0.95  # alfa: Tasa de aprendizaje
g = 0.05  # gamma: Factor de descuento
e = 0.01  # epsilon: para e-greedy

try:
    with open("q_values.json", "r") as file:
        Q_loaded = json.load(file)
    Q = {eval(key): value for key, value in Q_loaded.items()}
except FileNotFoundError:
    pass


def getR(state, action):
    reward = 0
    ydiff = state[0]
    lowerpipeX = state[1]
    vel = state[2]

    # si esta un poco por encima del pipe inferior (altura +o- perfecta)
    if ydiff == 4 and action:
        reward -= 1
    elif ydiff == 4 and not action:
        reward += 1
    # si esta bajo la pipe inferior (debe saltar)
    elif ydiff > 0 and action:
        reward += 1
    elif ydiff > 0 and not action:
        reward -= 1
    # si esta sobre la pipe inferior y el gap (no debe saltar)
    elif ydiff < -4 and action:
        reward -= 1
    elif ydiff < -4 and not action:
        reward += 1
    # si esta casi tocando el cielo
    if ydiff > 4 and action:
        reward -= 100
    if ydiff > 4 and not action:
        reward += 2
    # si es menor a 5 (cerca de la tuberia) y vel es mayor a 0 (va descendiendo) debe saltar
    if lowerpipeX < 5 and vel > 0 and action:
        reward += 10
    print(state, action, reward)
    return reward


# el estado actual del juego
# altura del pajaro y las pipes, dividido por 10 para tener menos estados,
# ya que no importa si la altura es unos px mas o menos
def getState(ydiff, lowerPipeX, vel):
    state = (ydiff // 10, int(lowerPipeX // 10), vel)
    return state


def egreedy(state):
    S = state
    if random.random() < e:
        A = random.choice([True, False])
    else:
        # Explotacion: seleccionar la accion con el valor Q maximo
        A = max([True, False], key=lambda action: Q.get((S, action), 0.0))

    return A


def sarsa(state, prevAction, nextAction, R, newState):
    S = state
    S2 = newState

    # Q con estado actual y accion anterior
    currentQ = Q.get((S, prevAction), 0.0)

    # Q con estado nuevo y siguiente accion
    nextQ = Q.get((S2, nextAction), 0.0)

    # Calcular el nuevo valor Q para el estado actual y la accion anterior (formula)
    newQ = currentQ + a * (R + g * nextQ - currentQ)

    # Actualizar el diccionario Q con el nuevo valor Q
    Q[(S, prevAction)] = newQ

    Q_converted = {str(key): value for key, value in Q.items()}
    with open("q_values.json", "w") as file:
        json.dump(Q_converted, file, indent=4, ensure_ascii=False)


def qLearning(state, prevAction, R, newState):
    S = state
    S2 = newState

    currentQ = Q.get((S, prevAction), 0.0)

    maxQ = max([Q.get((S2, action), 0.0) for action in [True, False]])

    newQ = currentQ + a * (R + g * maxQ - currentQ)

    Q[(S, prevAction)] = newQ
