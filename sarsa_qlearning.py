import random
import hashlib
from flappy import *

Q = {}  # Diccionario para almacenar Q's, guarda un par estado y accion (Q es el valor)
a = 1  # alfa: Tasa de aprendizaje
g = 0  # gamma: Factor de descuento
e = 0  # epsilon: para e-greedy


def getR(state, action):
    reward = 0
    # if state[0] == SCREENHEIGHT / 2:
    #     reward = 0
    # elif state[0] < SCREENHEIGHT / 2 and action:
    #     reward += -1
    # elif state[0] < SCREENHEIGHT / 2 and not action:
    #     reward += 1
    # elif state[0] > SCREENHEIGHT / 2 and action:
    #     reward += 1
    # elif state[0] > SCREENHEIGHT / 2 and not action:
    #     reward += -1
    # pipe_height = 320  # Altura de la tubería

    # pipetop = state[1] + 320
    # pipebot = state[2]
    # print(state[0], pipetop, pipebot)

    # # si el pajaro esta a la altura del pipe superior
    # if state[0] <= pipetop and action:
    #     reward -= 1
    # elif state[0] <= pipetop and not action:
    #     reward += 1
    # # si el pajaro esta a la altura del pipe inferior
    # if state[0] >= pipebot and action:
    #     reward += 1
    # elif state[0] >= pipebot and not action:
    #     reward -= 1

    # state[0] = playery (altura)
    # state[1] = altura donde comienza el pipe inferior
    # gap = 100
    playery = state[0]
    pipebot = state[1]
   
    # si esta un poco por encima del pipe inferior (altura +o- perfecta)
    if playery == pipebot - 4 and action:
        reward -= 1
    elif playery == pipebot - 4 and not action:
        reward += 1
    # si esta bajo la pipe inferior (debe saltar)
    elif playery > pipebot and action:
        reward += 1
    elif playery > pipebot and not action:
        reward -= 1
    # si esta sobre la pipe inferior y el gap (no debe saltar)
    elif playery < pipebot - 4 and action:
        reward -= 1
    elif playery < pipebot - 4 and not action:
        reward += 1
    # si esta casi tocando el cielo
    if playery < 5 and action:
        reward -= 10
    print(playery, pipebot, reward)
    return reward


# el estado actual del juego
# altura del pajaro y las pipes, dividido por 10 para tener menos estados,
# ya que no importa si la altura es unos px mas o menos
def getState(playery, upperPipe, lowerPipeY, lowerPipeX):
    state = (playery // 10, lowerPipeY // 10)
    return state


def egreedy(state):
    S = hash(state)
    if random.random() < e:
        A = random.choice([True, False])
    else:
        # Explotacion: seleccionar la accion con el valor Q maximo
        A = max([True, False], key=lambda action: Q.get((S, action), 0.0))

    return A


def hash(state):
    # Convertir el estado en str hasheable
    state_str = str(state)
    state_hash = hashlib.sha256(state_str.encode()).hexdigest()
    return state_hash


def sarsa(state, prevAction, nextAction, R, newState):
    # hash para que se pueda ocupar en un diccionario
    S = hash(state)
    S2 = hash(newState)

    # Q con estado actual y accion anterior
    currentQ = Q.get((S, prevAction), 0.0)

    # Q con estado nuevo y siguiente accion
    nextQ = Q.get((S2, nextAction), 0.0)

    # Calcular el nuevo valor Q para el estado actual y la accion anterior (formula)
    newQ = currentQ + a * (R + g * nextQ - currentQ)

    # Actualizar el diccionario Q con el nuevo valor Q
    Q[(S, prevAction)] = newQ


def qLearning(state, prevAction, R, newState):
    S = hash(state)
    S2 = hash(newState)
    currentQ = Q.get((S, prevAction), 0.0)

    maxQ = max([Q.get((S2, action), 0.0) for action in [True, False]])

    newQ = currentQ + a * (R + g * maxQ - currentQ)

    Q[(S, prevAction)] = newQ
