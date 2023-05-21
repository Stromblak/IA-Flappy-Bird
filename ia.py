from red import *
from sarsa_qlearning import *


def ia(playerFlapped, tuberias, x, y, velCaida):
    # opcion pa elegir
    # red
    red(tuberias, y, velCaida)

    # sarsa

    # qlearning

    return playerFlapped


saltar = False
state = None
prevAction = None


def algoritmos(
    sarsaOqlearning,
    playery,
    playerx,
    playerVelY,
    upperPipes,
    lowerPipes,
):
    global saltar, state, prevAction
    # SARSA
    if sarsaOqlearning:
        # ejecutar A
        saltar = prevAction
        # observar R, S'
        R = getR()
        newState = getState(playery, playerx, playerVelY, upperPipes, lowerPipes)

        # elegir A' de un S' (con epsilon-greedy)
        nextAction = egreedy(newState)

        # aplicar formula Q
        sarsa(state, prevAction, nextAction, R, newState)

        # actualizar
        state = newState
        prevAction = nextAction

    # Q-Learning
    else:
        # elegir A de un S (con epsilon-greedy)
        prevAction = egreedy(state)

        # ejecutar A
        saltar = prevAction

        # observar R, S'
        R = getR()
        newState = getState(playery, playerx, playerVelY, upperPipes, lowerPipes)

        # aplicar formula Q
        qLearning(state, prevAction, R, newState)

        # actualizar
        state = newState
