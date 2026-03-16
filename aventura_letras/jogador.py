"""
Classe do personagem jogador
"""
import pygame
from config import (COR_PERSONAGEM, PRETO, 
                    GRAVIDADE, FORCA_PULO, 
                    VELOCIDADE_HORIZONTAL,
                    LARGURA, ALTURA)
from typing import Iterable
from elementos import Plataforma


class Jogador(pygame.sprite.Sprite):
    """Personagem principal do jogo"""
    
    def __init__(self, x: int, y: int, *groups):
        super().__init__(*groups)

        self.pos_x = float(x)
        self.pos_y = float(y)

        self.image = pygame.Surface((40, 50))
        self.image.fill(COR_PERSONAGEM)
        
        # Adicionar um rosto simples
        pygame.draw.circle(self.image, PRETO, (12, 15), 3)  # Olho esquerdo
        pygame.draw.circle(self.image, PRETO, (28, 15), 3)  # Olho direito
        pygame.draw.arc(self.image, PRETO, (10, 20, 20, 15), 3.14, 0, 2)  # Sorriso
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Física
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.no_chao = False
        
    def update(self, plataformas: Iterable[Plataforma]) -> None:
        """Atualiza posição e física do jogador"""

        # -------------------------
        # Gravidade
        # -------------------------
        self.velocidade_y += GRAVIDADE

        # -------------------------
        # Movimento horizontal
        # -------------------------
        teclas = pygame.key.get_pressed()
        self.velocidade_x = 0

        if teclas[pygame.K_LEFT]:
            self.velocidade_x = -VELOCIDADE_HORIZONTAL
        if teclas[pygame.K_RIGHT]:
            self.velocidade_x = VELOCIDADE_HORIZONTAL

        # Pulo
        if teclas[pygame.K_SPACE] and self.no_chao:
            self.velocidade_y = FORCA_PULO
            self.no_chao = False

        # -------------------------
        # MOVIMENTO HORIZONTAL
        # -------------------------
        self.pos_x += self.velocidade_x
        self.rect.x = int(self.pos_x)

        # Corrigir colisão horizontal
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.velocidade_x > 0:  # Indo para direita
                    self.rect.right = plataforma.rect.left
                elif self.velocidade_x < 0:  # Indo para esquerda
                    self.rect.left = plataforma.rect.right
                self.pos_x = self.rect.x

        # -------------------------
        # MOVIMENTO VERTICAL
        # -------------------------
        self.pos_y += self.velocidade_y
        self.rect.y = int(self.pos_y)

        self.no_chao = False

        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):

                # Caindo
                if self.velocidade_y > 0:
                    self.rect.bottom = plataforma.rect.top
                    self.velocidade_y = 0
                    self.no_chao = True

                # Subindo (batendo a cabeça)
                elif self.velocidade_y < 0:
                    self.rect.top = plataforma.rect.bottom
                    self.velocidade_y = 0

                self.pos_y = self.rect.y

        # -------------------------
        # Limites horizontais
        # -------------------------
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos_x = self.rect.x

        if self.rect.right > LARGURA:
            self.rect.right = LARGURA
            self.pos_x = self.rect.x

        # -------------------------
        # Respawn se cair
        # -------------------------
        if self.rect.top > ALTURA:
            self.pos_x = 100
            self.pos_y = ALTURA - 150
            self.rect.x = int(self.pos_x)
            self.rect.y = int(self.pos_y)
            self.velocidade_y = 0
