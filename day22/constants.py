'''Screen constants'''
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
X_MARGIN = 60
Y_MARGIN = 20
X_MAX = (SCREEN_WIDTH - X_MARGIN)//2 
Y_MAX = (SCREEN_HEIGHT - Y_MARGIN)//2 
SCREEN_COLOR = 'black'

FPS = 30
UPDATE_TIME = 1/FPS

ELEMENTS_COLOR = 'white'
ELEMENTS_WIDTH = 5
DASHES_LENGHT = 5

'''Game constants'''
GAME_NAME = 'Guile Pong'
TIME_BETWEEN_MATCHES = 1

'''Pad constants'''
PAD_HEIGHT = 100
PAD_WIDTH = 10
RIGHT_PAD_POS = ((SCREEN_WIDTH-X_MARGIN)//2,0)
LEFT_PAD_POS = (-(SCREEN_WIDTH-X_MARGIN)//2,0)

PAD_COLOR = 'white'
PAD_SPEED = 0
PAD_SHAPE = 'square'

PAD_STEP = 20

'''String constants'''
LEFT = 'left'
RIGHT = 'right'
NONE = ''

'''Difficulty constants'''
EASY = 'easy'
MEDIUM = 'medium'
HARD = 'hard'
DEFAULT = MEDIUM
DEFAULT_MATCHES = 5

EASY_MODE = 5
MEDIUM_MODE = 10
HARD_MODE = 15

'''Ball constants'''
BALL_SIZE = 15
BALL_SHAPE = 'circle'
BALL_COLOR = 'white'
BALL_SPEED = 0

MIN_ANGLE = 20

'''Scoreboard constants'''
FONT_COLOR = 'white'
ALIGN = 'center'
FONT = 'courier'
FONT_SIZE = 30
FONT_TYPE = 'bold'

GAME_OVER_FONT_SIZE = 50
GAME_OVER_FONT_COLOR = 'red'

SCOREBOARD_PADY = 50

'''Turtle constants'''
STANDARD_SIZE = 20