import random
import hashlib


Q = {}  # Diccionario para almacenar los valores Q
a = 0.5  # alfa: Tasa de aprendizaje
g = 0.9  # gamma: Factor de descuento
e = 0.3  # epsilon: para e-greedy


def getR():
    return -100


def getState(playery, playerx, playerVelY, upperPipes, lowerPipes):
    state = (playery, playerx, playerVelY, tuple(upperPipes), tuple(lowerPipes))
    return state


def egreedy(state):
    S = hash(state)
    if random.random() < e:
        # Exploracion: seleccionar una accion aleatoria
        A = random.choice([True, False])
    else:
        # Explotacion: seleccionar la accion con el valor Q maximo
        A = max([True, False], key=lambda a: Q.get((S, a), 0.0))

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
