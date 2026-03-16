"""
Classes de elementos do cenário: Plataforma e Letra
"""
import pygame
import random
from config import (COR_PLATAFORMA, COR_PLATAFORMA_BORDA, 
                    COR_LETRA, COR_LETRA_BORDA, PRETO)

class Plataforma(pygame.sprite.Sprite):
    """Plataforma do cenário"""
    
    def __init__(self, x, y, largura, altura):
        super().__init__()
        self.image = pygame.Surface((largura, altura))
        self.image.fill(COR_PLATAFORMA)
        
        # Adicionar borda superior para dar efeito 3D
        pygame.draw.rect(self.image, COR_PLATAFORMA_BORDA, (0, 0, largura, 3))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Letra(pygame.sprite.Sprite):
    """Letra coletável"""
    
    def __init__(self, x, y, letra, fonte):
        super().__init__()
        self.letra = letra
        self.fonte = fonte
        self.image = pygame.Surface((50, 50))
        self.image.fill(COR_LETRA)
        
        # Borda da letra
        pygame.draw.rect(self.image, COR_LETRA_BORDA, (0, 0, 50, 50), 3)
        
        # Renderizar a letra
        texto = self.fonte.render(letra, True, PRETO)
        texto_rect = texto.get_rect(center=(25, 25))
        self.image.blit(texto, texto_rect)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Animação de flutuação
        self.pos_inicial_y = y
        self.tempo = random.randint(0, 100)
        
    def update(self):
        """Animação de flutuação"""
        self.tempo += 0.1
        self.rect.y = self.pos_inicial_y + 5 * pygame.math.Vector2(0, 1).rotate(self.tempo * 10).y
