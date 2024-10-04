import pygame
import random

# Configurações iniciais
width = 1200
height = 600
playerSpeed = 10
Ground_width = width * 2
Ground_height = 88
gravity = 10
jump_height = 15
player_size = (60, 60)
zombie_speed = 5 
zombie_size = (60, 60)

font_path1 = 'fontes/VCR_OSD_MONO_1.001.ttf'

# Inicializa o mixer
pygame.mixer.init()
pygame.mixer.music.load('sons/awesomeness.wav')  # Substitua pelo caminho da sua música
pygame.mixer.music.play(-1)  # -1 significa que a música vai tocar em loop

zombie_sound = pygame.mixer.Sound('sons/groan.wav')  # Substitua pelo caminho do som do zumbi



class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        def load_image(path):
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(image, player_size)

        # Animações para caminhar
        self.image_walk = [
            load_image('images/personagem1.png'),
            load_image('images/personagem2.png'),
            load_image('images/personagem3.png'),
        ]

        self.image_run = [
            load_image('images/personagemCorrendo1.png'),
            load_image('images/personagemCorrendo2.png'),
            load_image('images/personagemCorrendo3.png')
        ]
        
        # Animações para pular
        self.image_jump = [
            load_image('images/personagemPulo2.png'),
        ]
        
        # Animações para cair
        self.image_fall = [
            load_image('images/personagemCaindo1.png'),
        ]

        # Inicialmente, usa o primeiro sprite de andar
        self.image = self.image_walk[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (200, 460)
        self.current_image = 0
        self.jumping = False
        self.run = False
        self.jump_velocity = jump_height
        self.facing_right = True  # Direção em que o personagem está virado
        self.position_in_world = 200  # Posição do personagem no mundo, usada para colisões e lógica
        self.alive = True  # Verifica se o jogador está vivo

    def update(self, *args):
        if not self.alive:
            return  # Se o jogador está morto, não faz mais nada

        key = pygame.key.get_pressed()
        current_speed = playerSpeed + 10 if key[pygame.K_LSHIFT] else playerSpeed

        if key[pygame.K_d]:
            self.position_in_world += current_speed
            self.facing_right = True  # Virado para a direita

        if key[pygame.K_a]:
            self.position_in_world -= current_speed
            self.facing_right = False  # Virado para a esquerda

        # Controle de corrida
        self.run = key[pygame.K_LSHIFT]

        # Pulando apenas se a tecla espaço for pressionada e o personagem não estiver pulando
        if key[pygame.K_SPACE] and not self.jumping:
            self.jumping = True
            self.jump_velocity = jump_height

        # Lógica de animação - Animação de caminhada ou corrida
        if not self.jumping:  # Só anima se não estiver pulando ou caindo
            if key[pygame.K_a] or key[pygame.K_d]:
                if self.run:
                    self.current_image = (self.current_image + 1) % len(self.image_run)
                    self.image = self.image_run[self.current_image]
                else:
                    self.current_image = (self.current_image + 1) % len(self.image_walk)
                    self.image = self.image_walk[self.current_image]
            else:
                self.image = self.image_walk[0]  # Fica no sprite inicial se nenhuma tecla for pressionada

        # Animação de pulo
        if self.jumping:
            self.current_image = (self.current_image + 1) % len(self.image_jump)
            self.image = self.image_jump[self.current_image]
            self.rect[1] -= self.jump_velocity
            self.jump_velocity -= 2

        # Espelhar imagem se estiver virado para a esquerda (incluindo pulo)
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

        # Impede que o jogador caia além do chão
        if self.rect.bottom >= height - Ground_height + 10:
            self.rect.bottom = height - Ground_height + 10
            self.jumping = False  # Reseta o estado de pulo quando atinge o chão

        # Atualiza a posição do rect do jogador com base na posição mundial
        self.rect.x = 200  # Posição fixa do jogador na tela

    def die(self):
        self.alive = False
        self.image = pygame.Surface((0, 0))  # Faz o jogador desaparecer


# Ajuste a velocidade do zumbi no loop principal
def adjust_zombie_speed():
    if player.alive:  # Só ajuste a velocidade se o jogador estiver vivo
        base_speed = zombie_speed
        key = pygame.key.get_pressed()
        
        # Modifica a base_speed com base nas teclas pressionadas
        if key[pygame.K_LSHIFT]:
            base_speed += 1 
        if key[pygame.K_a]:
            return base_speed - 1 # Diminuir a velocidade do zumbi
        elif key[pygame.K_d]:
            return base_speed + 1  # Aumentar a velocidade do zumbi
        elif key[pygame.K_a] and key[pygame.K_d]:
            return 5
        return base_speed  # Velocidade padrão do zumbi

    return zombie_speed  # Retorna a velocidade padrão se o jogador não estiver vivo

class Zombie(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        
        def load_image(path):
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, zombie_size)
            return pygame.transform.flip(image, True, False)

        # Animação do zumbi andando
        self.image_walk = [
            load_image('images/ZombieCorre2.png'),
            load_image('images/ZombieCorre3.png'),
            load_image('images/ZombieCorre4.png'),
        ]

        # Sprite do zumbi morto
        self.image_dead = [
            load_image('images/ZombieMorte1.png'),
            load_image('images/ZombieMorte2.png'),
            load_image('images/ZombieMorte3.png'),
            load_image('images/ZombieMorte4.png'),
            load_image('images/ZombieMorte5.png'),
            load_image('images/ZombieMorte6.png'),
        ]

        self.image = self.image_walk[0]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (xpos, height - Ground_height + 10)
        self.current_image = 0
        self.alive = True
        self.dead_frame = 0

    def update(self, *args):
        if self.alive:
            self.current_image = (self.current_image + 1) % len(self.image_walk)
            self.image = self.image_walk[self.current_image]

            # Ajusta a velocidade dos zumbis apenas quando o jogador está vivo
            adjusted_speed = adjust_zombie_speed()
            self.rect.x -= adjusted_speed
        else:
            # Animação de morte
            if self.dead_frame < len(self.image_dead):
                self.image = self.image_dead[self.dead_frame]
                self.dead_frame += 1  # Avança a animação de morte
            else:
                # Remove o zumbi após a animação de morte
                self.kill()  # Remove o sprite do grupo

        # Ajusta a velocidade dos zumbis apenas quando o jogador está vivo
        adjusted_zombie_speed = adjust_zombie_speed() if player.alive else zombie_speed
        self.rect.x -= adjusted_zombie_speed
    
        # Ajusta a posição dos zumbis baseada na velocidade do jogador
        key = pygame.key.get_pressed()
        player_speed = playerSpeed + 10 if key[pygame.K_LSHIFT] else playerSpeed

        if key[pygame.K_d]:  # Jogador andando para a direita
            self.rect.x -= player_speed
        if key[pygame.K_a]:  # Jogador andando para a esquerda
            self.rect.x += player_speed

    def die(self):
        self.alive = False
        self.dead_frame = 0  # Reseta o contador de frames para a animação de morte
        zombie_sound.stop()  # Para o som do zumbi quando ele morrer

class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/ground.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (Ground_width, Ground_height))
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = height - Ground_height + 10

    def update(self, *args):
        if not player.alive:
            return  # Se o jogador está morto, o chão não se move mais

        key = pygame.key.get_pressed()
        current_speed = playerSpeed + 10 if key[pygame.K_LSHIFT] else playerSpeed
        if key[pygame.K_d] and player.rect.right < width:
            self.rect[0] -= current_speed
        if key[pygame.K_a] and player.rect.left > 0:
            self.rect[0] += current_speed


def is_off_screen(sprite):
    return sprite.rect.right < 0 or sprite.rect.left > width


# Função para exibir a mensagem "Game Over!"
def draw_game_over():
    pygame.mixer.music.stop()
    zombie_sound.stop()  # Para o som do zumbi quando ele morrer
    font = pygame.font.Font(font_path1, 50)  # Usando fonte personalizada
    text_game_over = font.render('Game Over!', True, (255, 255, 255))  # Texto em vermelho
    text_rect = text_game_over.get_rect(center=(width // 2, height // 2))
    game_window.blit(text_game_over, text_rect)

pygame.init()
game_window = pygame.display.set_mode([width, height])
pygame.display.set_caption('Jogo teste')

zombies_killed = 0

background = pygame.image.load('images/background.png').convert_alpha()
background = pygame.transform.scale(background, [width, height])

playerGroup = pygame.sprite.Group()
player = Player()
playerGroup.add(player)

groundGroup = pygame.sprite.Group()
for i in range(2):
    ground = Ground(Ground_width * i)
    groundGroup.add(ground)

zombieGroup = pygame.sprite.Group()

gameLoop = True

def draw():
    playerGroup.draw(game_window)
    groundGroup.draw(game_window)
    zombieGroup.draw(game_window)

    # Desenha o contador de zumbis mortos no canto superior esquerdo da tela
    font = pygame.font.Font(font_path1, 30)  # Usando a fonte personalizada
    counter_text = font.render(f'Zombies Killed: {zombies_killed}', True, (255, 255, 255))  # Texto em branco
    game_window.blit(counter_text, (10, 10))  # Posição do texto no canto superior esquerdo


def update():
    playerGroup.update()
    groundGroup.update()
    zombieGroup.update()


# Função para reiniciar o jogo
def reset_game():
    global player, zombieGroup, groundGroup

    # Reinicia o jogador
    player.kill()  # Remove o jogador atual
    player = Player()  # Cria um novo jogador
    playerGroup.add(player)

    # Reinicia o chão
    groundGroup.empty()  # Remove todos os blocos de chão
    for i in range(2):
        ground = Ground(Ground_width * i)
        groundGroup.add(ground)

    # Reinicia os zumbis
    zombieGroup.empty()  # Remove todos os zumbis

    # Reinicia a música de fundo
    pygame.mixer.music.play(-1)  # Recomeça a música


clock = pygame.time.Clock()
while gameLoop:
    clock.tick(20)
    game_window.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            gameLoop = False

        # Verifica se a tecla "r" foi pressionada para reiniciar o jogo
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            zombies_killed = 0
            reset_game()  # Reinicia o jogo

    # Só mova o chão e ajuste a velocidade se o jogador estiver vivo
    if player.alive:
        # Verifica se precisamos adicionar um novo bloco de chão à direita
        if groundGroup.sprites()[-1].rect.right <= width:
            newGround = Ground(groundGroup.sprites()[-1].rect.right)
            groundGroup.add(newGround)

        # Verifica se precisamos adicionar um novo bloco de chão à esquerda
        if groundGroup.sprites()[0].rect.left >= 0:
            newGround = Ground(groundGroup.sprites()[0].rect.left - Ground_width)
            groundGroup.add(newGround)

        # Remove o chão que saiu da tela
        for ground in groundGroup:
            if is_off_screen(ground):
                groundGroup.remove(ground)

        # Adiciona um novo zumbi se não houver muitos na tela
        if len(zombieGroup) < 1 and random.randint(1, 100) > 70:
            newZombie = Zombie(width)
            zombieGroup.add(newZombie)
            zombie_sound.play(-1)  # Toca o som do zumbi em loop

    # Checa colisões entre o jogador e os zumbis
    for zombie in zombieGroup:
        if zombie.alive and pygame.sprite.collide_rect(player, zombie):
            if player.jumping and player.rect.bottom <= zombie.rect.top + 10:
                zombie.die()
                zombies_killed += 1
            else:
                player.die()
                playerGroup.remove(player)
                pygame.mixer.music.stop()  # Para a música de fundo ao morrer
                zombie_sound.stop()  # Para o som do zumbi ao morrer
                break

    # Remove zumbis que saíram da tela à esquerda
    for zombie in zombieGroup:
        if is_off_screen(zombie):
            zombieGroup.remove(zombie)

    update()

    # Desenhar tudo se o jogador estiver vivo, senão desenhar apenas o Game Over
    if player.alive:
        draw()
    else:
        game_window.blit(background, (0, 0))  # Desenhar o fundo
        draw_game_over()  # Desenhar a mensagem de Game Over

    pygame.display.update()
