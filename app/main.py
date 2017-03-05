import bottle
import os
import random
import utils
import numpy as np

ID = 'PLACEHOLDER'
#foodCount = 0 # The number of foods on the board
# Previous state codes:
#   0 = finding food
#   1 = circling food
prevState = 0 

# --------Grid data-------
snakeHead = 0 # Head will be set as the length of the snake
snakeBody = -1
foodPos = -2
safePos = -3
# ------------------------


# Initialize our personal grid and other variables
def init(data):
    ourSnake = None
    grid = [ [0 for col in xrange(data['width'])] for row in xrange(data['height']) ]
    foodCount = len(data['food'])

    for snake in data['snakes']: # Loop through all snakes on the board
        if snake['id'] == data['you']:
            ourSnake = snake

        headCoord = snake['coords'][0] # head of snake
        grid[headCoord[0]][headCoord[1]] = utils.getSnakeLen(snake['coords']) # set grid pos of head to be length of snake

        for coord in snake['coords']: # Get the coordinates of the snake
            grid[coord[0]][coord[1]] = snakeBody # Set grid val to snake

    for food in data['food']: # Loop through all food on the board
        grid[food[0]][food[1]] = foodPos

    return ourSnake, grid, foodCount


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
        'name': 'Vulture Snake',
        'head_type': 'smile',
    	'tail_type': 'pixel'
    }

@bottle.post('/move')
def move():
    data = bottle.request.json

    ourSnake, grid, foodCount = init(data)
            
    #move, prevState = utils.newState(foodCount, prevState, ourSnake, data['food'])
   
    move = utils.getSeekMove(ourSnake, data) # TODO: Fix other states and cases
    
    return {
        'move': move,
        'taunt': 'Snek-caw!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
