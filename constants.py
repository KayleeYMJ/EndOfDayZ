""" Constants """

##---- Configurations ----##
TASK = 2
MAP_FILE = 'maps/basic4.txt'

# Characters that represent entities in a grid.
PLAYER = "P"
HOSPITAL = "H"
BORDER = "#"

ZOMBIE = "Z"
TRACKING_ZOMBIE = "T"
ZOMBIES = (ZOMBIE, TRACKING_ZOMBIE)

GARLIC = "G"
CROSSBOW = "C"
PICKUP_ITEMS = (GARLIC, CROSSBOW)
# Lifetimes of pickup items.
LIFETIMES = {GARLIC: 10, CROSSBOW: 5}

# Actions a player can perform.
UP = "W"
LEFT = "A"
DOWN = "S"
RIGHT = "D"
DIRECTIONS = (UP, LEFT, DOWN, RIGHT)
FIRE = "F"

# Direction offsets, see random_directions docstring for more details.
OFFSETS = [(-1, 0), (0, 1), (0, -1), (1, 0)]    # W, S, N, E

# User interaction constants.
ACTION_PROMPT = "Enter your next action: "
WIN_MESSAGE = "You win!"
LOSE_MESSAGE = "You lose!"

HOLDING_MESSAGE = "The player is currently holding:"
FIRE_PROMPT = "Direction to fire: "
NO_ZOMBIE_MESSAGE = "No zombie in that direction!"
INVALID_FIRING_MESSAGE = "Invalid firing direction entered!"
NO_WEAPON_MESSAGE = "You are not holding anything to fire!"


##---- GUI Constants ----##
# Task 1 Constants
TITLE = 'EndOfDayz'
INVENTORY_TITLE = 'Inventory'

MAP_WIDTH = MAP_HEIGHT = 400
MAX_ITEMS = 10
INVENTORY_COLS = 2
INVENTORY_WIDTH = 200

DARK_PURPLE = ACCENT_COLOUR = '#371D33'
DARKEST_PURPLE = '#371D33'
LIGHT_BROWN = MAP_BACKGROUND_COLOUR = '#B5B28F'
LIGHT_GREEN = '#B8D58E'
LIGHT_PURPLE = '#E5E1EF'
CELL_SIZE = 50

ENTITY_COLOURS = {
	PLAYER: DARK_PURPLE,
	HOSPITAL: DARK_PURPLE,
	ZOMBIE: LIGHT_GREEN,
	GARLIC: LIGHT_PURPLE,
	TRACKING_ZOMBIE: LIGHT_GREEN,
	CROSSBOW: LIGHT_PURPLE
}

# Task 2 Constants
BACK_GROUND = 'B'
ARROW = 'A'
BANNER = 'BA'
CHASER = 'CR'
CHASEE = 'CE'

IMAGES = {
	PLAYER:'images/hero.png',
	HOSPITAL:'images/hospital.png',
	ZOMBIE:'images/zombie.png',
	GARLIC:'images/garlic.png',
	TRACKING_ZOMBIE:'images/zombie.png',
	CROSSBOW:'images/crossbow.png',
        BANNER:'images/banner.png',
        CHASER:'images/chaser.png',
        CHASEE:'images/chasee.png',
	BACK_GROUND:'images/tileable_background.png',
	ARROW:'images/arrow.png'
}

BANNER_HEIGHT = 100
ARROWS_TO_DIRECTIONS = {'Left':LEFT, 'Right':RIGHT, 'Up':UP, 'Down':DOWN}

HIGH_SCORES_FILE = 'high_scores.txt'
MAX_ALLOWED_HIGH_SCORES = 3

TIMER = 'Timer'
MOVES_MADE = 'Moves made'
RESTART_GAME = 'Restart Game'
QUIT_GAME = 'Quit Game'
FILE = 'File'
QUIT = 'Quit'
SAVE_GAME = 'Save Game'
LOAD_GAME = 'Load Game'
HIGH_SCORES = 'High Scores'

WARNING = 'Warning'
WARNING_MESSAGE = 'Cannot find some information about a saved game. \n Please try again.'
QUIT_MESSAGE = 'Do you want to quit?'
SPACE = ' '


TIME_MACHINE = 'M'
