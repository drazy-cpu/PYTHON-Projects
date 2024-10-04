import pygame
import random

# Configurações do jogo
BOARD_WIDTH = 360
BOARD_HEIGHT = 640
PEDRO_WIDTH = 34
PEDRO_HEIGHT = 24
PIKA_WIDTH = 64
PIKA_HEIGHT = 512
GRAVITY = 0.7
VELOCITY_X = -4

# Estados do jogo
MENU, PLAYING, GAME_OVER = range(3)

# Inicializar Pygame e o mixer
pygame.init()
pygame.mixer.init()  # Inicializar o mixer
screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
pygame.display.set_caption("Bossordiney: The Cock Sucker")
clock = pygame.time.Clock()

# Carregar e redimensionar imagens
background_img = pygame.transform.scale(pygame.image.load("imagens/pedrobg.png"), (BOARD_WIDTH, BOARD_HEIGHT))
menu_background_img = pygame.transform.scale(pygame.image.load("imagens/pedro8bits.png"), (BOARD_WIDTH, BOARD_HEIGHT))
background_gameover_img = pygame.transform.scale(pygame.image.load("imagens/pedrobgGameover.png"), (BOARD_WIDTH, BOARD_HEIGHT))
pedro_img = pygame.transform.scale(pygame.image.load("imagens/pedro.png"), (PEDRO_WIDTH, PEDRO_HEIGHT))
top_pika_img = pygame.transform.scale(pygame.image.load("imagens/toppenis.png"), (PIKA_WIDTH, PIKA_HEIGHT))
bottom_pika_img = pygame.transform.scale(pygame.image.load("imagens/bottompenis.png"), (PIKA_WIDTH, PIKA_HEIGHT))

# Carregar músicas
menu_music = "sons/pedroStart.wav"
game_music = "sons/pedroSoundtrack.wav"
gameover_music = "sons/pedroGameover.wav"
# Carregar sons de efeito
score_up_sound = pygame.mixer.Sound("sons/pedroAutista.mp3")
# Carregar som de colisão
collision_sound = pygame.mixer.Sound("sons/pedroDano.mp3")

score_up_sound.set_volume(1.0)



# Definir volume
pygame.mixer.music.set_volume(0.5)  # Ajuste conforme necessário

# Pedro (personagem principal)
class Pedro:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PEDRO_WIDTH
        self.height = PEDRO_HEIGHT
        self.velocity_y = 0

    def move(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        self.y = max(self.y, 0)  # Limita o Pedro ao topo da tela

    def draw(self):
        screen.blit(pedro_img, (self.x, self.y))


# Pika (obstáculos)
class Pika:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.width = PIKA_WIDTH
        self.height = PIKA_HEIGHT
        self.img = img
        self.passed = False

    def move(self):
        self.x += VELOCITY_X

    def draw(self):
        screen.blit(self.img, (self.x, self.y))


# Função para gerar os obstáculos
def place_pikas(pikas):
    random_pika_y = -PIKA_HEIGHT // 4 - random.randint(0, PIKA_HEIGHT // 2)
    opening_space = BOARD_HEIGHT // 4

    top_pika = Pika(BOARD_WIDTH, random_pika_y, top_pika_img)
    bottom_pika = Pika(BOARD_WIDTH, random_pika_y + PIKA_HEIGHT + opening_space, bottom_pika_img)

    pikas.append(top_pika)
    pikas.append(bottom_pika)


# Função para verificar colisões
def check_collision(pedro, pika):
    return (pedro.x < pika.x + pika.width and
            pedro.x + pedro.width > pika.x and
            pedro.y < pika.y + pika.height and
            pedro.y + pedro.height > pika.y)


def draw_text_menu(text, size, x, y, color, outline_color=(0, 0, 0)):
    font = pygame.font.Font("fontes/Minecrafter.Reg.ttf", size)  # Usar a fonte personalizada
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))

    # Desenhar o contorno
    outline_surface = font.render(text, True, outline_color)
    outline_rect = outline_surface.get_rect(center=text_rect.center)

    # Desenhar o contorno em várias posições
    screen.blit(outline_surface, (outline_rect.x - 1, outline_rect.y))  # esquerda
    screen.blit(outline_surface, (outline_rect.x + 1, outline_rect.y))  # direita
    screen.blit(outline_surface, (outline_rect.x, outline_rect.y - 1))  # acima
    screen.blit(outline_surface, (outline_rect.x, outline_rect.y + 1))  # abaixo

    # Desenhar o texto principal
    screen.blit(text_surface, text_rect)

# Função para desenhar texto com fonte personalizada
def draw_text(text, size, x, y, color, outline_color=(0, 0, 0)):
    font = pygame.font.Font("fontes/Minecraftia.ttf", size)  # Usar a fonte personalizada
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))

    # Desenhar o contorno
    outline_surface = font.render(text, True, outline_color)
    outline_rect = outline_surface.get_rect(center=text_rect.center)

    # Desenhar o contorno em várias posições
    screen.blit(outline_surface, (outline_rect.x - 1, outline_rect.y))  # esquerda
    screen.blit(outline_surface, (outline_rect.x + 1, outline_rect.y))  # direita
    screen.blit(outline_surface, (outline_rect.x, outline_rect.y - 1))  # acima
    screen.blit(outline_surface, (outline_rect.x, outline_rect.y + 1))  # abaixo

    # Desenhar o texto principal
    screen.blit(text_surface, text_rect)
# Modificar as funções de exibição de texto para ajustar o contorno
def draw_text_blinking(text, size, x, y, color, show_text, outline_color=(0, 0, 0)):
    if show_text:
        draw_text(text, size, x, y, color, outline_color)

def game_loop():
    game_state = MENU
    score = 0
    pedro = Pedro(BOARD_WIDTH // 8, BOARD_HEIGHT // 2)
    pikas = []
    place_pika_timer = 0

    # Variáveis para controle da animação de piscar
    blink_timer = 0
    show_text = True  # Controla se o texto deve ser mostrado

    # Carregar música do menu e tocá-la
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1)  # Tocar música de menu em loop

    running = True
    game_over_music_playing = False  # Flag para controlar a música de game over

    while running:
        screen.fill((0, 0, 0))

        if game_state == MENU:
            screen.blit(menu_background_img, (0, 0))

            # Desenhar o texto "Pedro" no meio da tela
            draw_text_menu("Bossordiney", 40, BOARD_WIDTH // 2, 100, (255, 255, 0))  # Cor amarela
            draw_text_menu("The Cock Sucker", 25, BOARD_WIDTH // 2, 150, (255, 255, 0))  # Cor amarela

            # Atualiza o temporizador de piscar para o texto de início
            blink_timer += clock.get_time()
            if blink_timer >= 500:  # Muda a cada 500 milissegundos
                show_text = not show_text  # Alterna entre mostrar e não mostrar o texto
                blink_timer = 0  # Reseta o temporizador

            # Desenha o texto piscante se show_text for True
            if show_text:
                draw_text("Press 'Space' to start", 18, BOARD_WIDTH // 2, 450, (255, 255, 255))

        elif game_state == PLAYING:
            screen.blit(background_img, (0, 0))
            pedro.move()
            pedro.draw()

            # Gerar novos obstáculos
            if place_pika_timer <= 0:
                place_pikas(pikas)
                place_pika_timer = 1500  # tempo para gerar próximo conjunto de pikas

            place_pika_timer -= clock.get_time()

            for pika in pikas[:]:
                pika.move()
                pika.draw()

                # Verificar se Pedro passou pelos obstáculos
                if not pika.passed and pedro.x > pika.x + pika.width:
                    score += 0.5
                    pika.passed = True
                    score_up_sound.play()  # Tocar o som quando o score aumentar

                # Verificar colisões
                if check_collision(pedro, pika):
                    collision_sound.play()  # Tocar som de colisão
                    game_state = GAME_OVER

                # Remover obstáculos fora da tela
                if pika.x + pika.width < 0:
                    pikas.remove(pika)

            # Desenhar score
            draw_text(f" {int(score)}", 20, 20, 20, (0, 255, 0))

            # Verificar se Pedro caiu fora da tela
            if pedro.y > BOARD_HEIGHT:
                collision_sound.play()  # Tocar som de colisão
                game_state = GAME_OVER

            # Carregar e tocar a música do jogo apenas quando o estado mudar
            if game_state == PLAYING and not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(game_music)
                pygame.mixer.music.play(-1)  # Tocar música do jogo em loop

        elif game_state == GAME_OVER:
            screen.blit(background_gameover_img, (0, 0))  # Exibir o fundo de game over
            draw_text_menu("Game Over", 32, BOARD_WIDTH // 2, 80, (255, 255, 255))
            draw_text_menu(f"Cocks sucked: {int(score)}", 24, BOARD_WIDTH // 2, 120,
                           (255, 255, 255))

            # Tocar a música de Game Over apenas uma vez
            if not game_over_music_playing:
                pygame.mixer.music.load(gameover_music)  # Carregar a música de game over
                pygame.mixer.music.play(0)  # Tocar a música uma vez
                game_over_music_playing = True  # Marcar que a música de Game Over está tocando

            # Atualiza o temporizador de piscar para o texto de reinício
            blink_timer += clock.get_time()
            if blink_timer >= 500:  # Muda a cada 500 milissegundos
                show_text = not show_text  # Alterna entre mostrar e não mostrar o texto
                blink_timer = 0  # Reseta o temporizador

            # Desenha a mensagem piscante se show_text for True
            draw_text_blinking("Press 'R' to Restart", 20, BOARD_WIDTH // 2, BOARD_HEIGHT // 2 + 200,
                               (255, 255, 255), show_text)

        # Controle de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_state == MENU:
                    if event.key == pygame.K_SPACE:
                        game_state = PLAYING
                        pygame.mixer.music.stop()  # Parar a música de menu
                elif game_state == PLAYING:
                    if event.key == pygame.K_SPACE:
                        pedro.velocity_y = -9  # Pedro "pula"
                    elif event.key == pygame.K_ESCAPE:
                        game_state = MENU
                        pedro.y = BOARD_HEIGHT // 2
                        pedro.velocity_y = 0
                        pikas.clear()
                        score = 0
                        game_over_music_playing = False  # Resetar a flag
                        pygame.mixer.music.load(menu_music)  # Recarregar música do menu
                        pygame.mixer.music.play(-1)  # Reproduzir música de menu em loop
                elif game_state == GAME_OVER:
                    if event.key == pygame.K_r:  # 'R' reinicia o jogo
                        game_state = PLAYING
                        pedro.y = BOARD_HEIGHT // 2
                        pedro.velocity_y = 0
                        pikas.clear()
                        score = 0
                        game_over_music_playing = False  # Resetar a flag
                        pygame.mixer.music.load(game_music)  # Recarregar música do jogo
                        pygame.mixer.music.play(-1)  # Reproduzir música de jogo em loop
                    elif event.key == pygame.K_ESCAPE:  # ESC volta ao menu
                        game_state = MENU
                        pedro.y = BOARD_HEIGHT // 2
                        pedro.velocity_y = 0
                        pikas.clear()
                        score = 0
                        game_over_music_playing = False  # Resetar a flag
                        pygame.mixer.music.load(menu_music)  # Recarregar música do menu
                        pygame.mixer.music.play(-1)  # Reproduzir música de menu em loop

        pygame.display.flip()
        clock.tick(60)  # 60 frames por segundo

    pygame.quit()


    # Iniciar o jogo
if __name__ == "__main__":
     game_loop()
