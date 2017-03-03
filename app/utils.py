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
	#cirDist = ?
	# Determine the threshold of when to move to food
	thresh = dist+10

	# If no food on board...
	# If previous state was circling food and health < threshold --> eat food	
	# If previous state was circling food and health above threshold --> continue circling
	# If previous state was finding food and health above threshold and position is 'one' away from food --> start circling
	# If previous state was finding food and position is more than 'one' away from food --> continue finding food
	if foodCount == 0:
		#choose random?
		move = getDirection(snake) #TODO: replace w/ logic
	elif (health <= thresh) and (dist == 1):
		#move to toward food
		if snakeHead[0] > closeFood[0]:
			move = 'left'
		elif snakeHead[0] < closeFood[0]:
			move = 'right'
		elif snakeHead[1] > closeFood[1]:
			move = 'up'
		elif snakeHead[1] < closeFood[1]:
			move = 'down'
	elif (prevState == 1  or dist == cirDist) and (health > threshold):
		#call to function deciding next move in circling state
		move = getDefMove(snake)
	else: #prevState == 0:
		#call to function deciding next move in finding food state
		#move = getDirection(snake) #TODO: replace w/ logic
		move = getSeekMove(snake)
		#move = getOffMove(snakeHead, closeFood)
	
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

def getSeekMove(snake):
    move = None # Null checking?
    snakeHead = snek['coords'][0]
    x = snakeHead[0]
    y = snakeHead[1]
    direction = getDirection(snake)
    closeFood = closestFood(foods, snakeHead)
	# Determine the distance to the closest food
    dist = distance(snakeHead, closeFood)

    if foodCount == 0:
    		#choose random?
		move = getDirection(snake) #TODO: replace w/ logic
    else:
		#move to toward food
    	if snakeHead[0] > closeFood[0]:
			move = 'left'
     	elif snakeHead[0] < closeFood[0]:
			move = 'right'
        elif snakeHead[1] > closeFood[1]:
			move = 'up'
        elif snakeHead[1] < closeFood[1]:
			move = 'down'
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

def checkCollision(snake, grid, move):
	# under construction
	# move = "up" | "left" | "down" | "right"

	currentPos = snake['coords'][0]

