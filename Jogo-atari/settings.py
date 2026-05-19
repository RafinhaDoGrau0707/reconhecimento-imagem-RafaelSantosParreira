# settings.py

# Configurações da tela
WIDTH = 800
HEIGHT = 600
FPS = 60
TITLE = "Atari-style Space Shooter"

# Cores (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

# Configurações do jogador
PLAYER_SPEED = 8
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
PLAYER_COLOR = GREEN

# Configurações do asteroide
ASTEROID_MIN_SPEED = 2
ASTEROID_MAX_SPEED = 4
ASTEROID_WIDTH = 30
ASTEROID_HEIGHT = 30
ASTEROID_COLOR = GRAY
ASTEROID_SPAWN_RATE = 1500 # Tempo em milissegundos

# Configurações do projétil
PROJECTILE_SPEED = 10
PROJECTILE_WIDTH = 5
PROJECTILE_HEIGHT = 15
PROJECTILE_COLOR = YELLOW
