import pygame
import config

def desenhar_fundo(tela):
    largura_atual = tela.get_width()
    altura_atual = tela.get_height()
    tela.fill(config.VERDE_LOUSA)
    pygame.draw.rect(tela, config.MARROM_MADEIRA, (0, 0, largura_atual, altura_atual), 20)
    pygame.draw.rect(tela, (20, 60, 30), (20, 20, largura_atual-40, altura_atual-40), 2)

def desenhar_quadrado_letra(tela, fonte, letra, x, y, escala=1.0):
    tamanho_base = 70
    tamanho_real = int(tamanho_base * escala)
    offset = (tamanho_real - tamanho_base) // 2
    pos_x = x - offset
    pos_y = y - offset
    
    sombra_rect = (pos_x + 5, pos_y + 5, tamanho_real, tamanho_real)
    pygame.draw.rect(tela, (50, 30, 10), sombra_rect, border_radius=5)
    
    rect = (pos_x, pos_y, tamanho_real, tamanho_real)
    pygame.draw.rect(tela, config.MARROM_CLARO, rect, border_radius=5)
    pygame.draw.rect(tela, config.MARROM_MADEIRA, rect, 3, border_radius=5)
    
    if letra:
        texto = fonte.render(letra, True, config.BRANCO_GIZ)
        rect_texto = texto.get_rect(center=(pos_x + tamanho_real//2, pos_y + tamanho_real//2))
        tela.blit(texto, rect_texto)

def desenhar_underline(tela, x, y):
    pygame.draw.line(tela, config.BRANCO_GIZ, (x, y + 75), (x + 70, y + 75), 4)

# FUNÇÃO PARA O CRIAR O MENU 
def desenhar_botao(tela, texto, fonte, x, y, largura, altura, cor_fundo, cor_texto):
    """Desenha um botão retangular com texto centralizado"""
    rect = pygame.Rect(x, y, largura, altura)
    
    # Sombra do botão
    pygame.draw.rect(tela, (30, 20, 10), (x+4, y+4, largura, altura), border_radius=10)
    # Fundo do botão
    pygame.draw.rect(tela, cor_fundo, rect, border_radius=10)
    # Borda do botão
    pygame.draw.rect(tela, config.MARROM_MADEIRA, rect, 3, border_radius=10)
    
    # Texto
    txt = fonte.render(texto, True, cor_texto)
    tela.blit(txt, txt.get_rect(center=rect.center))