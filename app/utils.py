# Decide which state we want to be in for current move
# Previous state codes:
#	0 = finding food
#	1 = circling food
def newState(foodCount, prevState, snake, foods):
	# Get our snake's head position
	snakeX = snake['coords'][0]
	snakeY = snake['coords'][1]
	# Determine which food is the closest to use
	closeFood = closestFood(foods)
	# Determine the distance to the closest food
	dist = distance([snakeX, snakeY], closeFood)
	# Get our snakes health
	health = snake["health_points"]
	# Get our snakes length
	snakeLen = getSnakeLen(snake['coords'])
	# Determine the threshold of when to move to food
	thresh = determineThreshold(snakeLen, closeFood)

	# If no food on board...
	# If previous state was circling food and health < threshold --> eat food	
	# If previous state was circling food and health above threshold --> continue circling
	# If previous state was finding food and health above threshold and position is 'one' away from food --> start circling
	# If previous state was finding food and position is more than 'one' away from food --> continue finding food
	if foodCount == 0:
		#choose random?
	elif (health < thresh) and (dist == 1):
		#move to toward food	
	elif (prevState == 1) or (dist == 1):
		#call to function deciding next move in circling state	
	elif prevState == 0:
		#call to function deciding next move in finding food state
	else:
		#?

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

# Get the next cell coordinates based on a snake's direction
def getNextCell(snake):
	x1 = snake['coords'][0][0]
	y1 = snake['coords'][0][1]
	x2 = snake['coords'][1][0]
	y2 = snake['coords'][1][1]

	direction = getDirection(snake)

	if direction == 'right':
		return [x1 + 1, y1]
	elif direction == 'left':
		return [x1 - 1, y1]
	elif direction == 'down':
		return [x1, y1 + 1]
	elif direction == 'up':
		return [x1, y1 - 1]

def checkCollision(snake, grid, move):
	# under construction
	print 'we need a way to pass in the move that the snake is trying to make'

	currentPos = snake['coords'][0]
