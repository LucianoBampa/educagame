import pygame

# Configurações da tela
if not pygame.get_init():
    pygame.init()
info = pygame.display.Info()
LARGURA = info.current_w
ALTURA = info.current_h
FPS = 60

# Paleta de cores
COR_CEU = (135, 206, 250)
COR_GRAMA = (34, 139, 34)
COR_PLATAFORMA = (101, 67, 33)
COR_PLATAFORMA_BORDA = (139, 90, 43)
COR_PERSONAGEM = (255, 140, 0)
COR_LETRA = (255, 215, 0)
COR_LETRA_BORDA = (218, 165, 32)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE_SUCESSO = (46, 204, 113)
VERMELHO_ERRO = (231, 76, 60)
ROXO = (155, 89, 182)
AZUL_ESCURO = (52, 73, 94)

# Níveis de dificuldade
FACIL = "facil"
MEDIO = "medio"
DIFICIL = "dificil"

# Configurações de física do jogador
GRAVIDADE = 0.8
FORCA_PULO = -15
VELOCIDADE_HORIZONTAL = 5

# Configurações de plataformas por dificuldade
CONFIG_PLATAFORMAS = {
    FACIL: {
        'largura_base': 180,
        'largura_minima': 120,
        'salto_vertical': 70,
        'salto_h_min': 120,
        'salto_h_max': 180,
        'reducao_largura': 8
    },
    MEDIO: {
        'largura_base': 140,
        'largura_minima': 100,
        'salto_vertical': 85,
        'salto_h_min': 150,
        'salto_h_max': 220,
        'reducao_largura': 6
    },
    DIFICIL: {
        'largura_base': 110,
        'largura_minima': 80,
        'salto_vertical': 100,
        'salto_h_min': 180,
        'salto_h_max': 260,
        'reducao_largura': 5
    }
}

# Margens de segurança
MARGEM_ESQUERDA = 50
MARGEM_DIREITA = 50
MARGEM_SUPERIOR = 160
ALTURA_CHAO = 50
