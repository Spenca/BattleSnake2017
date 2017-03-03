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
