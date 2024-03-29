from itertools import cycle
import random
import sys
import pygame
from pygame.locals import *

SONIDO = False

FPS = 30.0
SCREENWIDTH  = 288
SCREENHEIGHT = 512
PIPEGAPSIZE  = 100 # gap between upper and lower part of pipe
BASEY        = SCREENHEIGHT * 0.79
# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
	# red bird
	(
		'../../assets/sprites/redbird-upflap.png',
		'../../assets/sprites/redbird-midflap.png',
		'../../assets/sprites/redbird-downflap.png',
	),
	# blue bird
	(
		'../../assets/sprites/bluebird-upflap.png',
		'../../assets/sprites/bluebird-midflap.png',
		'../../assets/sprites/bluebird-downflap.png',
	),
	# yellow bird
	(
		'../../assets/sprites/yellowbird-upflap.png',
		'../../assets/sprites/yellowbird-midflap.png',
		'../../assets/sprites/yellowbird-downflap.png',
	),
)

# list of backgrounds
BACKGROUNDS_LIST = (
	'../../assets/sprites/background-day.png',
	'../../assets/sprites/background-night.png',
)

# list of pipes
PIPES_LIST = (
	'../../assets/sprites/pipe-green.png',
	'../../assets/sprites/pipe-red.png',
)

xrange = range

def main2():
	global SCREEN, FPSCLOCK
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
	pygame.display.set_caption('Flappy Bird')

	# numbers sprites for score display
	IMAGES['numbers'] = (
		pygame.image.load('../../assets/sprites/0.png').convert_alpha(),
		pygame.image.load('../../assets/sprites/1.png').convert_alpha(),
		pygame.image.load('../../assets/sprites/2.png').convert_alpha(),
		pygame.image.load('../../assets/sprites/3.png').convert_alpha(),
		pygame.image.load('../../assets/sprites/4.png').convert_alpha(),
		pygame.image.load('../../assets/sprites/5.png').convert_alpha(),
		pygame.image.load('../../assets/sprites/6.png').convert_alpha(),
		pygame.image.load('../../assets/sprites/7.png').convert_alpha(),
		pygame.image.load('../../assets/sprites/8.png').convert_alpha(),
		pygame.image.load('../../assets/sprites/9.png').convert_alpha()
	)

	# game over sprite
	IMAGES['gameover'] = pygame.image.load('../../assets/sprites/gameover.png').convert_alpha()
	# message sprite for welcome screen
	IMAGES['message'] = pygame.image.load('../../assets/sprites/message.png').convert_alpha()
	# base (ground) sprite
	IMAGES['base'] = pygame.image.load('../../assets/sprites/base.png').convert_alpha()

	# sounds
	if 'win' in sys.platform:
		soundExt = '.wav'
	else:
		soundExt = '.ogg'

	SOUNDS['die']    = pygame.mixer.Sound('../../assets/audio/die' + soundExt)
	SOUNDS['hit']    = pygame.mixer.Sound('../../assets/audio/hit' + soundExt)
	SOUNDS['point']  = pygame.mixer.Sound('../../assets/audio/point' + soundExt)
	SOUNDS['swoosh'] = pygame.mixer.Sound('../../assets/audio/swoosh' + soundExt)
	SOUNDS['wing']   = pygame.mixer.Sound('../../assets/audio/wing' + soundExt)

	# select random background sprites
	randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
	IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

	# select random player sprites
	randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
	IMAGES['player'] = (
		pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
		pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
		pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
	)

	# select random pipe sprites
	pipeindex = random.randint(0, len(PIPES_LIST) - 1)
	IMAGES['pipe'] = (
		pygame.transform.flip(
			pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), False, True),
		pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
	)

	# hitmask for pipes
	HITMASKS['pipe'] = (
		getHitmask(IMAGES['pipe'][0]),
		getHitmask(IMAGES['pipe'][1]),
	)

	# hitmask for player
	HITMASKS['player'] = (
		getHitmask(IMAGES['player'][0]),
		getHitmask(IMAGES['player'][1]),
		getHitmask(IMAGES['player'][2]),
	)


	"""Shows welcome screen animation of flappy bird"""
	# index of player to blit on screen
	playerIndex = 0
	playerIndexGen = cycle([0, 1, 2, 1])
	# iterator used to change playerIndex after every 5th iteration
	loopIter = 0

	playerx = int(SCREENWIDTH * 0.2)
	playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)

	messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
	messagey = int(SCREENHEIGHT * 0.12)

	basex = 0
	# amount by which base can maximum shift to left
	baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

	# player shm for up-down motion on welcome screen
	playerShmVals = {'val': 0, 'dir': 1}

	# adjust playery, playerIndex, basex
	if (loopIter + 1) % 5 == 0:
		playerIndex = next(playerIndexGen)
	loopIter = (loopIter + 1) % 30
	basex = -((-basex + 4) % baseShift)

	# draw sprites
	SCREEN.blit(IMAGES['background'], (0,0))
	SCREEN.blit(IMAGES['player'][playerIndex],
				(playerx, playery + playerShmVals['val']))
	SCREEN.blit(IMAGES['message'], (messagex, messagey))
	SCREEN.blit(IMAGES['base'], (basex, BASEY))

	pygame.display.update()
	FPSCLOCK.tick(FPS)


# cosa principal
tubFin = 10000
MOVIMIENTO = 0

def mainGame(nets):
	pajaros = len(nets)
	score = playerIndex = loopIter = 0

	FPSCLOCK.tick(FPS)

	playerIndexGen = cycle([0, 1, 2, 1])
	playerx = [ int(SCREENWIDTH * 0.2) for i in range(pajaros)]
	playery = [ int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2) for i in range(pajaros)]

	basex = 0
	baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()


	gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE)) + int(BASEY * 0.2)
	upperPipes = [{'x': SCREENWIDTH + 200, 'y': gapY - IMAGES['pipe'][0].get_height()}]
	lowerPipes = [{'x': SCREENWIDTH + 200, 'y': gapY + PIPEGAPSIZE}]

	newPipe = getRandomPipe(lowerPipes)
	upperPipes.append(newPipe[0])
	lowerPipes.append(newPipe[1])

	dt = FPSCLOCK.tick(FPS)/1000.0
	pipeVelX = -128 * dt

	# player velocity, max velocity, downward acceleration, acceleration on flap
	playerVelY    =  [-9 for i in range(pajaros)]   # player's velocity along Y, default same as playerFlapped
	playerMaxVelY =  10   # max vel along Y, max descend speed
	playerMinVelY =  -8   # min vel along Y, max ascend speed
	playerAccY    =  1   # players downward acceleration
	playerRot     =  [45 for i in range(pajaros)]   # player's rotation
	playerVelRot  =  3   # angular speed
	playerRotThr  =  20   # rotation threshold
	playerFlapAcc =  -9   # players speed on flapping
	playerFlapped =  [False for i in range(pajaros)] # True when player flaps

	restantes     =  {i for i in range(pajaros)}
	fitness       =  [0 for i in range(pajaros)]
	distMuerte    =  [0 for i in range(pajaros)]

	tuberiaW  = IMAGES['pipe'][0].get_width()
	tuberiaH = IMAGES['pipe'][0].get_height()
	playerW = IMAGES['player'][0].get_width()
	playerH = IMAGES['player'][0].get_height()

	ciclo = 0
	delta = pipeVelX/4 * MOVIMIENTO

	while True:
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
		
			for i in restantes:
				if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
					if playery[i] > -2 * IMAGES['player'][0].get_height():
						playerVelY[i] = playerFlapAcc
						playerFlapped[i] = True
						if SONIDO:
							SOUNDS['wing'].play()	

		muertos = set()
		for i in restantes:
			pajaro = {"x": playerx[i], "y": playery[i], "velY": playerVelY[i], "h": playerH, "w": playerW}
			tuberias = {"tuberias": zip(upperPipes, lowerPipes), "h": tuberiaH, "w": tuberiaW}

			entrada = [pajaro["velY"] / 10.0]
			for uPipe, lPipe in tuberias["tuberias"]:
				if uPipe["x"] + tuberias["w"] <= pajaro["x"]:
					continue

				delta_Abajo  = (lPipe["y"]                           - pajaro["y"] + pajaro["h"]) / (322.0 - pajaro["h"])
				delta_Final  = (min(148, uPipe["x"]) + tuberias["w"] - pajaro["x"]              ) / (148.0)

				entrada.append( delta_Abajo )
				entrada.append( delta_Final )
				entrada.append(delta/(pipeVelX/4))
				break

			# ia
			if nets[i].activate(entrada)[0] >= 0.5:
				if playery[i] > -2 * IMAGES['player'][0].get_height():
					playerVelY[i] = playerFlapAcc
					playerFlapped[i] = True
					if SONIDO:
						SOUNDS['wing'].play()	

			# check for crash here
			crashTest, dist = checkCrash({'x': playerx[i], 'y': playery[i], 'index': playerIndex},
								upperPipes, lowerPipes)
		
			if crashTest[0]:
				muertos.add(i)
				distMuerte[i] = dist

			fitness[i] = score
			# rotate the player
			if playerRot[i] > -90:
				playerRot[i] -= playerVelRot

			# player's movement
			if playerVelY[i] < playerMaxVelY and not playerFlapped[i]:
				playerVelY[i] += playerAccY
			if playerFlapped[i]:
				playerFlapped[i] = False

			# more rotation to cover the threshold (calculated in visible rotation)
			playerRot[i] = 45
			playery[i] += min(playerVelY[i], BASEY - playery[i] - playerH)


		restantes -= muertos
		if len(restantes) <= 0 or score == tubFin:
			return fitness, distMuerte
		
		# check for score
		playerMidPos = int(SCREENWIDTH * 0.2) + IMAGES['player'][0].get_width() / 2
		for pipe in upperPipes:
			pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
			if pipeMidPos <= playerMidPos < pipeMidPos + 4:
				score += 1
				if SONIDO:
					SOUNDS['point'].play()


		# playerIndex basex change
		if (loopIter + 1) % 3 == 0:
			playerIndex = next(playerIndexGen)
		loopIter = (loopIter + 1) % 30
		basex = -((-basex + 100) % baseShift)


		# move pipes to left
		for uPipe, lPipe in zip(upperPipes, lowerPipes):
			uPipe['x'] += pipeVelX
			lPipe['x'] += pipeVelX
			

		# movimiento tuberias	----------------------------------------------------------
		if not (ciclo % FPS):
			delta *= -1
		ciclo += 1
		for uPipe, lPipe in zip(upperPipes, lowerPipes):
			if delta > 0 and lPipe['y'] + delta <= 322:
				uPipe['y'] += delta
				lPipe['y'] += delta

			if delta < 0 and uPipe['y'] + delta >= -260:
				uPipe['y'] += delta
				lPipe['y'] += delta

		

		# add new pipe when first pipe is about to touch left of screen
		if 3 > len(upperPipes) > 0 and 0 < upperPipes[0]['x'] < 5:
			newPipe = getRandomPipe(lowerPipes)
			upperPipes.append(newPipe[0])
			lowerPipes.append(newPipe[1])

		# remove first pipe if its out of the screen
		if len(upperPipes) > 0 and upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
			upperPipes.pop(0)
			lowerPipes.pop(0)

		# draw sprites
		SCREEN.blit(IMAGES['background'], (0,0))

		for uPipe, lPipe in zip(upperPipes, lowerPipes):
			SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
			SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

		SCREEN.blit(IMAGES['base'], (basex, BASEY))
		# print score so player overlaps the score
		showScore(score)
		showPoblacion(len(restantes))

		# Player rotation has a threshold
		visibleRot = playerRotThr
		if playerRot[i] <= playerRotThr:
			visibleRot = playerRot[i]
		
		playerSurface = pygame.transform.rotate(IMAGES['player'][playerIndex], visibleRot)

		for i in restantes:
			SCREEN.blit(playerSurface, (playerx[i], playery[i]))

		pygame.display.update()

def getRandomPipe(lowerPipes):
	gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
	gapY += int(BASEY * 0.2)
	pipeHeight = IMAGES['pipe'][0].get_height()
	pipeX = lowerPipes[-1]["x"] + SCREENWIDTH/2 + 4

	return [
		{'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
		{'x': pipeX, 'y': gapY + PIPEGAPSIZE}, # lower pipe
	]


def checkCrash(player, upperPipes, lowerPipes):
	"""returns True if player collides with base or pipes."""
	pi = player['index']
	player['w'] = IMAGES['player'][0].get_width()
	player['h'] = IMAGES['player'][0].get_height()

	distMuerte = 0

	# if player crashes into ground
	if player['y'] + player['h'] >= BASEY - 1:
		distMuerte = 2000
		return [True, True], distMuerte
	
	elif player['y'] < 0:
		distMuerte = 1000
		return [True, True], distMuerte
	
	else:
		playerRect = pygame.Rect(player['x'], player['y'],
					player['w'], player['h'])
		pipeW = IMAGES['pipe'][0].get_width()
		pipeH = IMAGES['pipe'][0].get_height()

		for uPipe, lPipe in zip(upperPipes, lowerPipes):
			# upper and lower pipe rects
			uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
			lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

			# player and upper/lower pipe hitmasks
			pHitMask = HITMASKS['player'][pi]
			uHitmask = HITMASKS['pipe'][0]
			lHitmask = HITMASKS['pipe'][1]

			# if bird collided with upipe or lpipe
			uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
			lCollide = pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)


			if uCollide or lCollide:
				distMuerte = abs( (lPipe['y'] - PIPEGAPSIZE/2) - (player['y'] + player['h']/2))

				return [True, False], distMuerte

	return [False, False], distMuerte

def pixelCollision(rect1, rect2, hitmask1, hitmask2):
	"""Checks if two objects collide and not just their rects"""
	rect = rect1.clip(rect2)

	if rect.width == 0 or rect.height == 0:
		return False

	x1, y1 = rect.x - rect1.x, rect.y - rect1.y
	x2, y2 = rect.x - rect2.x, rect.y - rect2.y

	for x in xrange(rect.width):
		for y in xrange(rect.height):
			if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
				return True
	return False

def getHitmask(image):
	"""returns a hitmask using an image's alpha."""
	mask = []
	for x in xrange(image.get_width()):
		mask.append([])
		for y in xrange(image.get_height()):
			mask[x].append(bool(image.get_at((x,y))[3]))
	return mask



def showScore(score):
	"""displays score in center of screen"""
	scoreDigits = [int(x) for x in list(str(score))]
	totalWidth = 0 # total width of all numbers to be printed

	for digit in scoreDigits:
		totalWidth += IMAGES['numbers'][digit].get_width()

	Xoffset = (SCREENWIDTH - totalWidth) / 2

	for digit in scoreDigits:
		SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
		Xoffset += IMAGES['numbers'][digit].get_width()

def showPoblacion(score):
	"""displays score in center of screen"""
	scoreDigits = [int(x) for x in list(str(score))]
	totalWidth = 0 # total width of all numbers to be printed

	for digit in scoreDigits:
		totalWidth += IMAGES['numbers'][digit].get_width()

	Xoffset = (SCREENWIDTH - totalWidth) / 2

	for digit in scoreDigits:
		SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.02))
		Xoffset += IMAGES['numbers'][digit].get_width()
