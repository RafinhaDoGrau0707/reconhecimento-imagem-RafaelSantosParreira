import pygame
import sys
from settings import *
from sprites import Player, Asteroid

class Game:
    def __init__(self):
        # Inicializa o pygame e cria a janela
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 48)
        self.running = True

    def new(self):
        # Inicia um novo jogo
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        self.player = Player()
        self.all_sprites.add(self.player)

        self.last_asteroid_spawn = pygame.time.get_ticks()
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        # Trata todos os eventos do jogo (teclas apertadas, fechar janela, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            # Evento isolado para atirar: disparar apenas uma vez a cada pressionamento
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    proj = self.player.shoot()
                    self.all_sprites.add(proj)
                    self.projectiles.add(proj)

    def update(self):
        # Atualiza o estado de todos os sprites
        self.all_sprites.update()

        # Calcula a dificuldade dinamicamente baseada na pontuação
        difficulty_multiplier = 1.0 + (self.score / 200.0)
        
        # Aumenta a frequência de asteroides diminuindo o tempo entre spawns
        current_spawn_rate = max(300, int(ASTEROID_SPAWN_RATE / difficulty_multiplier))

        now = pygame.time.get_ticks()
        if now - self.last_asteroid_spawn > current_spawn_rate:
            self.last_asteroid_spawn = now
            asteroid = Asteroid(difficulty_multiplier)
            self.all_sprites.add(asteroid)
            self.asteroids.add(asteroid)

        # Colisão Projétil contra Asteroide (True e True significa que ambos somem)
        hits = pygame.sprite.groupcollide(self.asteroids, self.projectiles, True, True)
        for hit in hits:
            self.score += 10 # Aumenta a pontuação

        # Colisão Jogador contra Asteroide
        hits = pygame.sprite.spritecollide(self.player, self.asteroids, False)
        if hits:
            self.playing = False # Fim de jogo
            
        # Verifica se algum asteroide passou do fundo da tela
        for asteroid in self.asteroids:
            if asteroid.rect.top > HEIGHT:
                self.playing = False # Fim de jogo

    def draw(self):
        # Limpa a tela com preto
        self.screen.fill(BLACK)
        
        # Desenha todos os sprites na tela
        self.all_sprites.draw(self.screen)
        
        # Renderiza e desenha a pontuação no canto superior esquerdo
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Atualiza a tela (double buffering do Pygame)
        pygame.display.flip()

    def show_game_over_screen(self):
        if not self.running:
            return
            
        # Tela de fim de jogo
        self.screen.fill(BLACK)
        game_over_text = self.font.render("GAME OVER", True, RED)
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        restart_text = self.font.render("Press any key to restart", True, WHITE)
        
        # Centraliza os textos
        self.screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//3))
        self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        self.screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT * 2//3))
        pygame.display.flip()
        
        # Espera o jogador apertar alguma tecla para reiniciar ou fechar
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

if __name__ == '__main__':
    game = Game()
    while game.running:
        game.new()
        if game.running:
            game.show_game_over_screen()
    pygame.quit()
    sys.exit()
