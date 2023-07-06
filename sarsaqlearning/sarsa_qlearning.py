import random
from flappy import *
import json

Q = {}  # Diccionario para almacenar Q's, guarda un par estado y accion (Q es el valor)
a = 0.7  # alfa: Tasa de aprendizaje #0.7 0.8 0.9
g = 0.95  # gamma: Factor de descuento #0.95 1
e = 0  # epsilon: para e-greedy #0 0.1

try:
    with open("./sarsaqlearning/qqq.json", "r") as file:
        Q_loaded = json.load(file)
    Q = {eval(key): value for key, value in Q_loaded.items()}
except FileNotFoundError:
    pass


def saveqvalues():
    Q_converted = {str(key): value for key, value in Q.items()}
    with open("./sarsaqlearning/qqq.json", "w") as file:
        json.dump(Q_converted, file, indent=4, ensure_ascii=False)


# el estado actual del juego
# altura del pajaro y las pipes, dividido por 10 para tener menos estados,
# ya que no importa si la altura es unos px mas o menos
def getState(ydiff, xdiff, vel):
    state = (ydiff // 10, int(xdiff // 10), vel)
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
            else:
                A = only_action
        else:
            A = max(
                [True, False],
                key=lambda action: Q.get((state, action), random.choice([True, False])),
            )
    return A


def sarsa(state, prevAction, nextAction, R, newState):
    # Q con estado actual y accion anterior
    currentQ = Q.get((state, prevAction), 0.0)

    # Q con estado nuevo y siguiente accion
    nextQ = Q.get((newState, nextAction), 0.0)

    # Calcular el nuevo valor Q para el estado actual y la accion anterior (formula)
    newQ = currentQ + a * (R + g * nextQ - currentQ)

    # Actualizar el diccionario Q con el nuevo valor Q
    Q[(state, prevAction)] = newQ


def qLearning(state, prevAction, R, newState):
    currentQ = Q.get((state, prevAction), False)

    maxQ = max([Q.get((newState, action), False) for action in [True, False]])

    newQ = currentQ + a * (R + g * maxQ - currentQ)

    Q[(state, prevAction)] = newQ


def save_epi_scr(episode, score):
    with open("datas.txt", "a") as file:
        file.write(f"{episode} {score}\n")
