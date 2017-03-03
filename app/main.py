import bottle
import os
import random
import utils

ID = 'PLACEHOLDER'
foodCount = 0 # The number of foods on the board

# --------Grid data-------
snakeHead = 0 # Head will be set as the length of the snake
snakeBody = -1
foodPos = -2
safePos = -3
# ------------------------


# Initialize our personal grid and other variables
def init(data):
    grid = [ [0 for col in xrange(data['width'])] for row in xrange(data['height']) ]
    foodCount = len(data['food'])

    ourSnake = snake['you'] # See if it's us

    for snake in data['snakes']: # Loop through all snakes on the board

        headCoord = snake['coords'][0] # head of snake
        grid[headCoord[0]][headCoord[1]] = utils.getSnakeLen(snake['coords']) # set grid pos of head to be length of snake

        for coord in snake['coords']: # Get the coordinates of the snake
            grid[coord[0]][coord[1]] = snakePos # Set grid val to snake

    for food in data['food']: # Loop through all food on the board
        grid[food[0]][food[1]] = foodPos

    return ourSnake, grid

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#000000',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'Vulture Snake'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    init(data)

    directions = ['up', 'down', 'left', 'right']

    return {
        'move': random.choice(directions),
        'taunt': 'Snek-caw!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
