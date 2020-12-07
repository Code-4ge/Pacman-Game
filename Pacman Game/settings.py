from pygame.math import Vector2 as vec

# screen settings
WIDTH, HEIGHT = 610, 670
FPS = 60
TOP_BOTTOM_BUFFER = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH-TOP_BOTTOM_BUFFER, HEIGHT-TOP_BOTTOM_BUFFER
SQUARE = 20
ROWS = 30
COLS = 28

# colour settings
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (107, 107, 107)
WHITE = (255, 255, 255)
PLAYER_COLOUR = (255, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PINK = (255, 105, 180)
ORANGE = (255, 165, 0)
BLUE = (44, 167, 198)

# font settings
START_TEXT_SIZE = 16
START_FONT = 'arial black'

# resource settings
BLINKY = 'Assets/rghost.png'
PINKY = 'Assets/pghost.png'
INKY = 'Assets/bghost.png'
CLYDE = 'Assets/oghost.png'
