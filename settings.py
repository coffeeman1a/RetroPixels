# game settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
TILE_SIZE = 16
LAYERS = {
    'ground': 8,
    'walls': 9,
    'main': 11,
    'items': 12
}

TEXTURE_PATH = {
    'player': 'sprites/player.png',
    'standing_torch': 'sprites/standing_torch_animation.png',
    'wooden_chest': 'RetroCoff1/wooden_chest.png'
}

CAN_BE_PLACED_ON = ['skull']

DEFAULT_ANIMATIONS = {
    'standing_torch': {'idle': [], 'extinguished': []},
    'wooden_chest': {'idle': [], 'opened': []}
}

ANIMATION_FRAMES = {
    'standing_torch': {'idle': [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)]},
    'wooden_chest': {'idle': [(0, 0)],
                     'opened': [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0)]}
}

# [[size], [inflate]]
OBJECTS_SIZE = {
    'standing_torch': [(16, 48), (-80, -260)],
    'walls': [(16, 16), (0, 0)],
    'doors': [(16, 16), (0, 0)],
    'wooden_barrel': [(16, 16), (-40, -20)],
    'skull': [(16, 16), (-20, -20)],
    'wooden_chest': [(16, 16), (-10, -65)]
}

OBJECTS_SCALE = {
    'skull': (4, 4)
}

HITBOX_OFFSETS = {
    'standing_torch': (0, 20)
}

SOUND_PATH = {
    'player_step': 'sounds/player/generic_footsteps.wav'
}

MUSIC_PATH = {
    'first_level': 'sounds/music/first_level.wav'
}

GAME_FONT = 'font/monogram-extended.ttf'

INVENTORY_ITEMS = {
    'empty': 0
}
