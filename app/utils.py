import random

# Decide which state we want to be in for current move
# Previous state codes:
#	0 = finding food
#	1 = circling food
def newState(foodCount, prevState, snake, foods):
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
	thresh = cirDist+10

	# If previous state was circling food and health < threshold --> eat food	
	# If previous state was circling food and health above threshold --> continue circling
	# If previous state was finding food and health above threshold and position is 'one' away from food --> start circling
	# If previous state was finding food and position is more than 'one' away from food --> continue finding food
	if (prevState == 1  or dist == 1) and (health > threshold):
		#call to function deciding next move in circling state
		move = getDefMove(snake)
		state = 1
	else: #prevState == 0:
		#call to function deciding next move in finding food state
		#move = getDirection(snake) #TODO: replace w/ logic
		move = getSeekMove(snake)
		state = 0
		#move = getOffMove(snakeHead, closeFood)
	
	return move, state

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

    if checkCollision(snake, data, move) == True:
		move = desperation(snake, data, move)
    		
    return move

# Get the side length of the min. incomplete square that can be formed by a snake of length n
def getSqSideLen(n):
	return 1 + ((n+4)/4)

# Get the move required to keep the snake in a defensive square formation around a food item
def getDefMove(snake):
	x = snake['coords'][0][0]
	y = snake['coords'][0][1]
	direction = getDirection(snake)
	
	squareDim = getSqSideLen(getSnakeLen(snake['coords']))	
	pt = snake['coords'][squareDim - 1]

	if direction == 'right':
		if pt == [x - squareDim + 1, y]:
			return 'down'
		else:
			return 'right'
	elif direction == 'left':
		if pt == [x + squareDim - 1, y]:
			return 'up'
		else:
			return 'left'
	elif direction == 'down':
		if pt == [x, y - squareDim + 1]:
			return 'left'
		else:
			return 'down'
	elif direction == 'up':
		if pt == [x, y + squareDim - 1]:
			return 'right'
		else:
			return 'up'

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
	opts.remove(move)
	for item in opts:
		if checkCollision(snake, data, item) == True:
			opts.remove(item)
	if len(opts) > 0:
		return random.choice(opts)
	return 'up'

def checkCollision(snake, data, move):
	# under construction
	# move = 'up' | 'left' | 'down' | 'right'
	# move translated to coordinates = [0, -1] | [-1, 0] | [0, 1] | [1, 0]
	# return true or false

	currentPos = snake['coords'][0]
	
	if move == 'up':
		choice = [currentPos[0], currentPos[1] - 1]

	if move == 'down':
		choice = [currentPos[0], currentPos[1] + 1]

	if move == 'right':
		choice = [currentPos[0] + 1, currentPos[1]]

	if move == 'left':
		choice = [currentPos[0] - 1, currentPos[1]]
	
	occupiedPositions = snake['coords'][1:] # snake body

	for s in data['snakes']: # other snakes
  		for c in s['coords']:
			occupiedPositions.append(c)

	for s in range(data['width']): # north and south walls
		occupiedPositions.append([s, -1])
		occupiedPositions.append([s, data['height']])
  
  	for s in range(data['height']): # east and west walls
  		occupiedPositions.append([-1, s])
  		occupiedPositions.append([data['width'], s])

  	if currentPos in occupiedPositions:
  		return True
  	else:
  		return False
