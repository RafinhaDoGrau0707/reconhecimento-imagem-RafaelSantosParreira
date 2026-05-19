import pygame
import random
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Cria a imagem (superfície) da nave como um retângulo simples
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        # Posiciona a nave na parte inferior central da tela
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        # Movimenta a nave com as setas esquerda e direita
        if keys[pygame.K_LEFT]:
            self.speed_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.speed_x = PLAYER_SPEED

        self.rect.x += self.speed_x

        # Limitar o movimento do jogador às bordas da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        # Instancia e retorna um novo projétil no topo da nave
        projectile = Projectile(self.rect.centerx, self.rect.top)
        return projectile


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, difficulty_multiplier=1.0):
        super().__init__()
        # Cria a imagem do asteroide
        self.image = pygame.Surface((ASTEROID_WIDTH, ASTEROID_HEIGHT))
        self.image.fill(ASTEROID_COLOR)
        self.rect = self.image.get_rect()
        # Sorteia uma posição no topo, fora da tela, e uma velocidade constante
        self.rect.x = random.randint(0, WIDTH - ASTEROID_WIDTH)
        self.rect.y = random.randint(-100, -40)
        
        # Aumenta a velocidade baseando-se no multiplicador de dificuldade
        min_speed = int(ASTEROID_MIN_SPEED * difficulty_multiplier)
        max_speed = int(ASTEROID_MAX_SPEED * difficulty_multiplier)
        self.speed_y = random.randint(min_speed, max_speed)

    def update(self):
        # Movimentação constante para baixo
        self.rect.y += self.speed_y


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Cria a imagem do projétil
        self.image = pygame.Surface((PROJECTILE_WIDTH, PROJECTILE_HEIGHT))
        self.image.fill(PROJECTILE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -PROJECTILE_SPEED

    def update(self):
        # Movimentação constante para cima
        self.rect.y += self.speed_y
        # Remove o projétil da memória se ele sair da tela
        if self.rect.bottom < 0:
            self.kill()
