import pygame

class Lutador():
    def __init__(self, jogador, x, y, virar, data, planilha, animation_steps, som):
        self.jogador = jogador
        self.tamanho = data[0]
        self.escala_imagem = data[1]
        self.virar = virar
        self.desvio = data[2]
        self.animation_list = self.load_images(planilha, animation_steps)
        self.acao = 0#0:idle #1:correndo #2:pulando #3:attack1 #4:attack2 #5:hit #6:morto
        self.frame_index = 0
        self.image = self.animation_list[self.acao][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.correndo = False
        self.pulo = False
        self.atacando = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_som = som
        self.hit = False
        self.vida = 100
        self.vivo = True


    def load_images(self, planilha, animation_steps):
      #extrair imagens da planilha
      animation_list = []
      for y, animation in enumerate(animation_steps):
        frame_list = []
        for x in range(animation):
          frame = planilha.subsurface(x * self.tamanho, y * self.tamanho, self.tamanho, self.tamanho)
          frame_list.append(pygame.transform.scale(frame, (self.tamanho * self.escala_imagem, self.tamanho * self.escala_imagem)))
        animation_list.append(frame_list)
      return animation_list


    def move(self, LARGURA_TELA, ALTURA_TELA, surface, target, round_over):
      VELOCIDADE = 10
      GRAVIDADE = 2
      dx = 0
      dy = 0
      self.correndo = False
      self.attack_type = 0

      #obter pressionamento de tecla
      tecla = pygame.key.get_pressed()

      #só poder realizar outras ações se não estiver atacando no momento
      if self.atacando == False and self.vivo == True and round_over == False:
          #verifique os controles do jogador 1
          if self.jogador == 1:
              #movimentação
              if tecla[pygame.K_a]:
                  dx = -VELOCIDADE
                  self.correndo = True
              if tecla[pygame.K_d]:
                  dx = VELOCIDADE
                  self.correndo = True
              #Pulo
              if tecla[pygame.K_w] and self.pulo == False:
                  self.vel_y = -30
                  self.pulo = True
              #ataque
              if tecla[pygame.K_r] or tecla[pygame.K_t]:
                self.ataque(target)
                #determinar qual tipo de ataque foi usado
                if tecla[pygame.K_r]:
                   self.attack_type = 1
                if tecla[pygame.K_t]:
                   self.attack_type = 2


          #verifique os controles do jogador 2
          if self.jogador == 2:
             #movimentação
             if tecla[pygame.K_LEFT]:
               dx = -VELOCIDADE
               self.correndo = True
             if tecla[pygame.K_RIGHT]:
               dx = VELOCIDADE
               self.correndo = True
             #Pulo
             if tecla[pygame.K_UP] and self.pulo == False:
               self.vel_y = -30
               self.pulo = True
             #ataque
             if tecla[pygame.K_KP1] or tecla[pygame.K_KP2]:
               self.ataque(target)
               #determinar qual tipo de ataque foi usado
               if tecla[pygame.K_KP1]:
                 self.attack_type = 1
               if tecla[pygame.K_KP2]:
                 self.attack_type = 2

      #aplicar gravidade
      self.vel_y += GRAVIDADE
      dy += self.vel_y

      #garantir que o jogador permaneça na tela
      if self.rect.left + dx < 0:
        dx = -self.rect.left
      if self.rect.right + dx > LARGURA_TELA:
          dx = LARGURA_TELA - self.rect.right
      if self.rect.bottom + dy > ALTURA_TELA - 110:
        self.vel_y = 0
        self.pulo = False
        dy = ALTURA_TELA - 110 - self.rect.bottom

      #garantir que os jogadores se enfrentem
      if target.rect.centerx > self.rect.centerx:
        self.virar = False
      else:
        self.virar = True

      #aplicar tempo de espera pra atacar novamente
      if self.attack_cooldown > 0:
        self.attack_cooldown -= 1

      #atualização de posição do jogador
      self.rect.x += dx
      self.rect.y += dy


    #lidar com atualização de animação
    def update(self):
      #verifica qual ação o jogador está realizando
      if self.vida <= 0:
        self.vida = 0
        self.vivo = False
        self.update_acao(6)#6: morto
      elif self.hit == True:
        self.update_acao(5)#5: hit
      elif self.atacando == True:
        if self.attack_type == 1:
          self.update_acao(3)#3: ataque1
        elif self.attack_type == 2:
          self.update_acao(4)#4: ataque2
      elif self.pulo == True:
        self.update_acao(2)#2: pulo
      elif self.correndo == True:
        self.update_acao(1)#1: correr
      else:
        self.update_acao(0)#0: idle
      animation_cooldown = 50
      # Atualizar imagem
      self.image = self.animation_list[self.acao][self.frame_index]
      # verifique se já passou tempo suficiente desde a última atualização
      if pygame.time.get_ticks() - self.update_time > animation_cooldown:
        self.frame_index += 1
        self.update_time = pygame.time.get_ticks()
      #verificar se a animação terminou
      if self.frame_index >= len(self.animation_list[self.acao]):
        #se o jogador estiver morto, então deverá terminar a animação
        if self.vivo == False:
          self.frame_index = len(self.animation_list[self.acao]) - 1
        else:
          self.frame_index = 0
          #verificar se um ataque foi executado
          if self.acao == 3 or self.acao == 4:
            self.atacando = False
            self.attack_cooldown = 30
          #verifique se o dano foi sofrido
          if self.acao == 5:
            self.hit = False
            #se o jogador estava no meio de um ataque, então o ataque é interrompido
            self.atacando = False
            self.attack_cooldown = 30



    def ataque(self, target):
      if self.attack_cooldown == 0:
        #executar ataque
        self.atacando = True
        self.attack_som.play()
        atacando_reto = pygame.Rect(self.rect.centerx - (4* self.rect.width * self.virar), self.rect.y, 4 * self.rect.width, self.rect.height)
        if atacando_reto.colliderect(target.rect):
          target.vida -= 10
          target.hit = True


    def update_acao(self, nova_acao):
      #verifica se a nova ação é diferente da anterior
      if nova_acao != self.acao:
        self.acao = nova_acao
        #atualize as configurações de animação
        self.frame_index = 0
        self.update_time - pygame.time.get_ticks()

    def desenhar(self, surface):
        img = pygame.transform.flip(self.image, self.virar, False)
        surface.blit(img, (self.rect.x - (self.desvio[0] * self.escala_imagem), self.rect.y - (self.desvio[1] * self.escala_imagem)))
