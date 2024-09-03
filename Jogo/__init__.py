import pygame
from pygame import mixer
from luta import Lutador

mixer.init()
pygame.init()

#Criando a janela do jogo
LARGURA_TELA = 1000
ALTURA_TELA = 600

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Lutador")

#definir FPS (taxa de quadros)
clock = pygame.time.Clock()
FPS = 60

#definir cores
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#definir variáveis do jogo
introducao_contador = 3
last_count_update = pygame.time.get_ticks()
pontuacao = [0, 0]  #pontuação do jogador. [J1, J2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#definir variáveis de lutador
ESPADACHIM_TAMANHO = 200
ESPADACHIM_ESCALA = 3.5
ESPADACHIM_DESVIO = [88, 70]
ESPADACHIM_DATA = [ESPADACHIM_TAMANHO, ESPADACHIM_ESCALA, ESPADACHIM_DESVIO]
MAGO_TAMANHO = 250
MAGO_ESCALA = 3
MAGO_DESVIO = [112, 107]
MAGO_DATA = [MAGO_TAMANHO, MAGO_ESCALA, MAGO_DESVIO]

#carregar música e sons
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
espada_fx = pygame.mixer.Sound("assets/audio/sword.wav")
espada_fx.set_volume(0.5)
magia_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magia_fx.set_volume(0.75)

#carregar imagem de fundo
fundo_imagem = pygame.image.load(
    "assets/imagens/tela de fundo/ufma_pixelart.png").convert_alpha()

#carregar imagens dos lutadores
espadachim_planilha = pygame.image.load(
    "assets/imagens/Espadachim/Sprites/espadachim.png").convert_alpha()
mago_planilha = pygame.image.load(
    "assets/imagens/Mago/Sprites/wizard.png").convert_alpha()

#carregar imagem de vitória
vitoria_img = pygame.image.load(
    "assets/imagens/icones/victory.png").convert_alpha()

#definir o número de etapas em cada animação
ESPADACHIN_ANIMATION_STEPS = [8, 8, 1, 6, 6, 4, 6]
MAGO_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

#definir fonte
count_fonte = pygame.font.Font("assets/fontes/turok.ttf", 80)
pontuacao_fonte = pygame.font.Font("assets/fontes/turok.ttf", 30)


#funcao para desenhar em texto
def desenhar_texto(texto, fonte, texto_col, x, y):
  img = fonte.render(texto, True, texto_col)
  tela.blit(img, (x, y))


#função para desenhar fundo
def desenhar_fundo():
  dimensao_fundo = pygame.transform.scale(fundo_imagem,
                                          (LARGURA_TELA, ALTURA_TELA))
  tela.blit(dimensao_fundo, (0, 0))


#função para desenhar barras de vida dos lutadores
def desenhar_barra_de_vida(vida, x, y):
  proporcao = vida / 100
  pygame.draw.rect(tela, WHITE, (x - 2, y - 2, 404, 34))
  pygame.draw.rect(tela, RED, (x, y, 400, 30))
  pygame.draw.rect(tela, YELLOW, (x, y, 400 * proporcao, 30))


#criação das duas instâncias de lutadores
lutador_1 = Lutador(1, 200, 310, False, ESPADACHIM_DATA, espadachim_planilha,
                    ESPADACHIN_ANIMATION_STEPS, espada_fx)
lutador_2 = Lutador(2, 700, 310, True, MAGO_DATA, mago_planilha,
                    MAGO_ANIMATION_STEPS, magia_fx)

#game loop
run = True
while run:

  clock.tick(FPS)

  #desenhar fundo
  desenhar_fundo()

  #mostrar estatísticas do jogador
  desenhar_barra_de_vida(lutador_1.vida, 20, 20)
  desenhar_barra_de_vida(lutador_2.vida, 580, 20)
  desenhar_texto("J1: " + str(pontuacao[0]), pontuacao_fonte, RED, 20, 60)
  desenhar_texto("J2: " + str(pontuacao[1]), pontuacao_fonte, RED, 580, 60)
  #contagem regressiva de atualização
  if introducao_contador <= 0:
    # mover lutadores
    lutador_1.move(LARGURA_TELA, ALTURA_TELA, tela, lutador_2, round_over)
    lutador_2.move(LARGURA_TELA, ALTURA_TELA, tela, lutador_1, round_over)
  else:
    #display do temporizador de contagem
    desenhar_texto(str(introducao_contador), count_fonte, RED,
                   LARGURA_TELA / 2, ALTURA_TELA / 3)
    #atualizar temporizador de contagem
    if (pygame.time.get_ticks() - last_count_update) >= 1000:
      introducao_contador -= 1
      last_count_update = pygame.time.get_ticks()

  #atualizar lutadores
  lutador_1.update()
  lutador_2.update()

  #desenhar lutadores
  lutador_1.desenhar((tela))
  lutador_2.desenhar((tela))

  #verifique a derrota do jogador
  if round_over == False:
    if lutador_1.vivo == False:
      pontuacao[1] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
    elif lutador_2.vivo == False:
      pontuacao[0] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
  else:
    #display imagem de vitória
    tela.blit(vitoria_img, (360, 150))
    if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
      round_over = False
      introducao_contador = 4
      lutador_1 = Lutador(1, 200, 310, False, ESPADACHIM_DATA,
                          espadachim_planilha, ESPADACHIN_ANIMATION_STEPS,
                          espada_fx)
      lutador_2 = Lutador(2, 700, 310, True, MAGO_DATA, mago_planilha,
                          MAGO_ANIMATION_STEPS, magia_fx)

  #manipulador de eventos
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  #exibição de atualização
  pygame.display.update()

#exit pygame
pygame.quit()
