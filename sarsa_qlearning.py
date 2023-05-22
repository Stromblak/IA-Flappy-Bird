import random
import hashlib
from flappy import SCREENHEIGHT

Q = {}  # Diccionario para almacenar los valores Q, guarda un par estado y accion (Q es el valor)
a = 1  # alfa: Tasa de aprendizaje
g = 0  # gamma: Factor de descuento
e = 0.1  # epsilon: para e-greedy


def getR(state, action):
    if state == SCREENHEIGHT / 2:
        reward = 0
    elif state < SCREENHEIGHT / 2 and action:
        reward = -1
    elif state < SCREENHEIGHT / 2 and not action:
        reward = 1
    elif state > SCREENHEIGHT / 2 and action:
        reward = 1
    elif state > SCREENHEIGHT / 2 and not action:
        reward = -1
    return reward


def getState(playery, playerx, playerVelY, upperPipes, lowerPipes):
    state = playery
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

    # implementar max alfa A, algo ???
    nextQ = Q.get((S2, a), 0.0)

    newQ = currentQ + a * (R + g * nextQ - currentQ)

    Q[(S, prevAction)] = newQ
