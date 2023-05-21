import random
import hashlib

Q = {}  # Diccionario para almacenar los valores Q
a = 0.5  # alfa: Tasa de aprendizaje
g = 0.9  # gamma: Factor de descuento
e = 0.3  # epsilon: para e-greedy


def getR():
    return 1.0


def getState(playery, playerx, playerVelY, upperPipes, lowerPipes):
    state = (playery, playerx, playerVelY, tuple(upperPipes), tuple(lowerPipes))
    return state


def hash(state):
    # Convertir el estado en str hasheable
    state_str = str(state)
    state_hash = hashlib.sha256(state_str.encode()).hexdigest()
    return state_hash


def sarsa(state, prevAction, newState):
    # hash para que se pueda ocupar en un diccionario
    S = hash(state)
    St = hash(newState)

    # Q con estado actual y accion anterior
    currentQ = Q.get((S, prevAction), 0.0)

    # Elegir siguiente accion con estado newState de Q
    if random.random() < e:
        # Exploracion: seleccionar una accion aleatoria
        nextAction = random.choice([True, False])
    else:
        # Explotacion: seleccionar la accion con el valor Q maximo
        nextAction = max([True, False], key=lambda a: Q.get((St, a), 0.0))

    # Q con estado nuevo y siguiente accion
    nextQ = Q.get((St, nextAction), 0.0)

    R = getR()
    # Calcular el nuevo valor Q para el estado actual y la accion anterior (formula)
    newQ = currentQ + a * (R + g * nextQ - currentQ)

    # Actualizar el diccionario Q con el nuevo valor Q
    Q[(S, prevAction)] = newQ

    return nextAction


def qLearning(state, prevAction, newState):
    S = hash(state)
    St = hash(newState)

    currentQ = Q.get((S, prevAction), 0.0)

    if random.random() < e:
        nextAction = random.choice([True, False])
    else:
        nextAction = max([True, False], key=lambda a: Q.get((St, a), 0.0))

    nextQ = Q.get((St, nextAction), 0.0)

    R = getR()
    
    newQ = currentQ + a * (R + g * nextQ - currentQ)

    Q[(S, prevAction)] = newQ

    return nextAction
