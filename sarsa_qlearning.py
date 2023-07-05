import random
from flappy import *
import json
import math

Q = {}  # Diccionario para almacenar Q's, guarda un par estado y accion (Q es el valor)
a = 0.8  # alfa: Tasa de aprendizaje
g = 1  # gamma: Factor de descuento
e = 0.01  # epsilon: para e-greedy

try:
    with open("q.json", "r") as file:
        Q_loaded = json.load(file)
    Q = {eval(key): value for key, value in Q_loaded.items()}
except FileNotFoundError:
    pass


def getR(state, action):
    reward = 0.5
    ydiff = state[0]
    lowerpipeX = state[1]
    vel = state[2]

    # # si esta un poco por encima del pipe inferior (altura +o- perfecta)
    # if ydiff == 4 and action:
    #     reward -= 1
    # elif ydiff == 4 and not action:
    #     reward += 1
    # # si esta bajo la pipe inferior (debe saltar)
    # elif ydiff > 0 and action:
    #     reward += 1
    # elif ydiff > 0 and not action:
    #     reward -= 1
    # # si esta sobre la pipe inferior y el gap (no debe saltar)
    # elif ydiff < -4 and action:
    #     reward -= 1
    # elif ydiff < -4 and not action:
    #     reward += 1
    # # si esta casi tocando el cielo
    # if ydiff > 4 and action:
    #     reward -= 100
    # if ydiff > 4 and not action:
    #     reward += 2
    # print(state, action, reward)
    return reward


def discretize(num):
    return 10 * math.floor(num / 10)


# el estado actual del juego
# altura del pajaro y las pipes, dividido por 10 para tener menos estados,
# ya que no importa si la altura es unos px mas o menos
def getState(ydiff, lowerPipeX, vel):
    state = (discretize(ydiff), discretize(lowerPipeX), vel)
    return state


def egreedy(state):
    # random
    if random.random() < e:
        A = random.choice([True, False])
    else:
        state_actions = [True, False]
        # Obtener todas las acciones para el estado dado
        actions_for_state = [action for action in state_actions if (state, action) in Q]

        # Verificar si solo hay una acción para el estado dado
        if len(actions_for_state) == 1:
            only_action = actions_for_state[0]
            q_value = Q[(state, only_action)]
            if q_value < 0:
                A = not only_action
                # print(state, q_value, only_action, A)
            else:
                A = only_action
        else:
            A = max(
                [True, False],
                key=lambda action: Q.get((state, action), random.choice([True, False])),
            )
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

    # Q_converted = {str(key): value for key, value in Q.items()}
    # with open("q_values.json", "w") as file:
    #     json.dump(Q_converted, file, indent=4, ensure_ascii=False)


def saveqvalues():
    Q_converted = {str(key): value for key, value in Q.items()}
    with open("q.json", "w") as file:
        json.dump(Q_converted, file, indent=4, ensure_ascii=False)


def qLearning(state, prevAction, R, newState):
    S = state
    S2 = newState

    currentQ = Q.get((S, prevAction), False)

    maxQ = max([Q.get((S2, action), False) for action in [True, False]])

    newQ = currentQ + a * (R + g * maxQ - currentQ)

    Q[(S, prevAction)] = newQ
