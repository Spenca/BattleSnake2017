import random

state = 0
sqCorners = [[0,0], [0,0], [0,0], [0,0]]

# Decide which state we want to be in for current move
# Previous state codes:
#	0 = finding food
#	1 = circling food
def newState(foodCount, snake, data):
    global state
    global sqCorners
    print sqCorners
    foods = data['food']
	# Get our snake's head position
    snakeHead = snake['coords'][0]
	# Determine which food is the closest to use
    closeFood = closestFood(foods, snakeHead)
	# Determine the distance to the closest food
    dist = distance(snakeHead, closeFood)
	# Get our snakes health
    health = snake["health_points"]
	# Get our snakes length
    snakeLen = getSnakeLen(snake['coords'])
	# Determine what distance away from the food we will circle at
	#cirDist = getSqSideLen(snakeLen)/2
	# Determine the threshold of when to move to food
    threshold = dist + 5

	# If previous state was circling food and health < threshold --> eat food	
	# If previous state was circling food and health above threshold --> continue circling
	# If previous state was finding food and health above threshold and position is 'one' away from food --> start circling
	# If previous state was finding food and position is more than 'one' away from food --> continue finding food

    if state == 0 and dist == 1 and health > threshold:
		#call to function defining square formation and deciding next move to enter circling state
		sqCorners, move = getSqCorners(snake, closeFood)
		state = 1
    elif state == 1 and health > threshold:
		#call to function deciding next move in circling state
		move = getDefMove(snake, sqCorners)
		state = 1
    else: #state == 0:
		#call to function deciding next move in finding food state
		#move = getDirection(snake) #TODO: replace w/ logic
		move = getSeekMove(snake, data)
		state = 0
		#move = getOffMove(snakeHead, closeFood)

    if checkCollision(snake, data, move) == True:
		move = desperation(snake, data, move)

    return move

# Get the length of a snake
def getSnakeLen(coords):
	return len(coords)

# Get the distance between two points
def distance(p, q):
    dx = abs(p[0] - q[0])
    dy = abs(p[1] - q[1])
    return dx + dy

# Find the closest piece of food in relation to position
def closestFood(foodList, position):
	closestFood = None
	closestDist = 9999

	for food in foodList:
		dist = distance(food, position)
		if dist < closestDist:
			closestFood = food
			closestDist = dist

	return closestFood

# Get the direction a snake is facing
def getDirection(snake):
	fst = snake['coords'][0]
	snd = snake['coords'][1]
	dx = fst[0] - snd[0]
	dy = fst[1] - snd[1]
	
	if dx == 1:
		return 'right'
	elif dx == -1:
		return 'left'
	elif dy == 1:
		return 'down'
	elif dy == -1:
		return 'up'
	return

#TODO: Fix case where snake turns into istelf
#TODO: Add transition to defense state     
def getSeekMove(snake, data):
	move = None # Null checking?
	snakeHead = snake['coords'][0]
	foodList = data['food']
	x = snakeHead[0]
	y = snakeHead[1]

	#direction = getDirection(snake)
	closeFood = closestFood(foodList, snakeHead)
	# Determine the distance to the closest food
	#dist = distance(snakeHead, closeFood)

	if snakeHead[0] > closeFood[0]:
		move = 'left'
	elif snakeHead[0] < closeFood[0]:
		move = 'right'
	elif snakeHead[1] > closeFood[1]:
		move = 'up'
	elif snakeHead[1] < closeFood[1]:
		move = 'down'
	
	print "I am moving: " + move
	return move

# Get the side length of the min. incomplete square that can be formed by a snake of length n
def getSqSideLen(n):
	return 1 + ((n+4)/4)

# Get an array of length 4 of the coordinates that define the defensive square: [top-left, top-right, bottom-right, bottom-left]
def getSqCorners(snake, closeFood):
	squareDim = getSqSideLen(getSnakeLen(snake['coords']))

	sX = snake['coords'][0][0]
	sY = snake['coords'][0][1]

	snakeHead = snake['coords'][0]

	dx = closeFood[0] - snakeHead[0]
	dy = closeFood[1] - snakeHead[1]

	if dx == 1:
		# food is right of head, closest corner is bottom left
		return [[sX,sY-squareDim+2], [sX+squareDim-1,sY-squareDim+2], [sX+squareDim-1, sY+1], [sX, sY+1]], 'up'
	elif dx == -1:
		# food is left of head, closest corner is top right
		return [[sX-squareDim+1, sY-1], [sX, sY-1], [sX, sY+squareDim-2], [sX-squareDim+1, sY+squareDim-2]], 'down'
	elif dy == 1:
		# food is below head, closest corner is top left
		return [[sX-1, sY], [sX+squareDim-2, sY], [sX+squareDim-2, sY+squareDim-1], [sX-1, sY+squareDim-1]], 'right'
	elif dy == -1:
		# food is above head, closest corner is bottom right
		return [[sX-squareDim+2, sY-squareDim+1], [sX+1, sY-squareDim+1], [sX+1, sY], [sX-squareDim+2, sY]], 'left'

def turnRight(direction):
	if direction == 'right':
		return 'down'
	elif direction == 'left':
		return 'up'
	elif direction == 'up':
		return 'right'
	elif direction == 'down':
		return 'left'

# Get the move required to keep the snake in a defensive square formation around a food item
def getDefMove(snake, sqCorners):

	snakeHead = snake['coords'][0]
	direction = getDirection(snake)

	if snakeHead in sqCorners:
		return turnRight(direction)
	else:
		return direction



#TODO: replace w/ better logic
def getOffMove(snakeHead, closeFood):
	if snakeHead[0] > closeFood[0]:
		move = 'left'
	elif snakeHead[0] < closeFood[0]:
		move = 'right'
	elif snakeHead[1] > closeFood[1]:
		move = 'up'
	elif snakeHead[1] < closeFood[1]:
		move = 'down'
	return move

# Return a collision free move
def desperation(snake, data, move):
	opts = ['up', 'down', 'right', 'left']
	print "1: " + str(opts)
	opts.remove(move)
	print "2: " + str(opts)
	bad = []
	for item in opts:
		if checkCollision(snake, data, item) == True:
			bad.append(item)
	remove_common_elements(opts, bad)
	if len(opts) > 0:
		return random.choice(opts)
	return 'left'

def remove_common_elements(a, b):
	for e in a[:]:
		if e in b:
			a.remove(e)

def checkCollision(snake, data, move):
	# under construction
	# move = 'up' | 'left' | 'down' | 'right'
	# move translated to coordinates = [0, -1] | [-1, 0] | [0, 1] | [1, 0]
	# return true or false

	currentPos = snake['coords'][0]
	
	if move == 'up':
		choice = [currentPos[0], currentPos[1] - 1]
	elif move == 'down':
		choice = [currentPos[0], currentPos[1] + 1]
	elif move == 'right':
		choice = [currentPos[0] + 1, currentPos[1]]
	else:
		choice = [currentPos[0] - 1, currentPos[1]]
	
	occupiedPositions = []

	for s in data['snakes']: # all snakes
  		for c in s['coords']:
			occupiedPositions.append(c)

	for s in range(data['width']): # north and south walls
		occupiedPositions.append([s, -1])
		occupiedPositions.append([s, data['height']])
  
  	for s in range(data['height']): # east and west walls
  		occupiedPositions.append([-1, s])
  		occupiedPositions.append([data['width'], s])

  	if choice in occupiedPositions:
  		return True
  	else:
  		return False
