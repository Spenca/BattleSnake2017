import bottle
import os
import random

ID = 'PLACEHOLDER'
snakeHead = 0 # Head will be set as the length of the snake
snakeBody = -1
foodPos = -2
safePos = -3

# Initialize our personal grid
def init(data):
    grid = [ [0 for col in xrange(data['width'])] for row in xrange(data['height']) ]

    for snake in data['snakes']: # Loop through all snakes on the board
        if snake['id'] == ID: # See if it's us
            ourSnake = snake
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

    directions = ['up', 'down', 'left', 'right']

    return {
        'move': random.choice(directions),
        'taunt': 'Snek-caw!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
