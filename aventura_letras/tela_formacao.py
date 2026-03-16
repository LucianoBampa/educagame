"""
Tela onde o jogador forma a palavra coletada
"""
import pygame
from config import (ROXO, BRANCO, COR_LETRA, COR_LETRA_BORDA, PRETO,
                    VERDE_SUCESSO, VERMELHO_ERRO,
                    LARGURA)


class TelaFormacao:
    """Tela onde o jogador forma a palavra"""
    
    def __init__(self, letras_coletadas, palavra_correta):
        self.letras_disponiveis = letras_coletadas.copy()
        self.palavra_formada = []
        self.palavra_correta = palavra_correta
        self.correto = False
        self.mensagem = ""
        self.tentativas = 0
        
    def adicionar_letra(self, letra):
        """Adiciona letra à palavra formada"""
        if letra in self.letras_disponiveis:
            self.palavra_formada.append(letra)
            self.letras_disponiveis.remove(letra)
            if not self.correto:
                self.mensagem = ""
            
    def remover_ultima(self):
        """Remove última letra da palavra"""
        if self.palavra_formada:
            letra = self.palavra_formada.pop()
            self.letras_disponiveis.append(letra)
            if not self.correto:
                self.mensagem = ""
            
    def verificar(self):
        """Verifica se a palavra está correta"""
        palavra = ''.join(self.palavra_formada)
        if palavra == self.palavra_correta:
            self.correto = True
            self.mensagem = "PARABÉNS! Você acertou!"
            return True
        else:
            self.tentativas += 1
            self.mensagem = "Ops! Tente novamente."
            return False
            
    def desenhar(self, tela, fonte_titulo, fonte_grande, fonte_media, fonte_pequena, 
                pontuacao_total, pontuacao_nivel):
        """Desenha a tela de formação"""
        tela.fill(ROXO)

        # Painel superior
        painel = pygame.Surface((LARGURA, 100))
        painel.fill((0, 40, 90))  # azul escuro
        painel.set_alpha(200)
        tela.blit(painel, (0, 0))

        # Pontuação total acumulada
        texto_total = fonte_media.render(
            f"Total: {pontuacao_total + pontuacao_nivel}",
            True,
            (255, 255, 255)
        )
        tela.blit(texto_total, (LARGURA - 300, 20))

        # Pontos do nível atual
        texto_nivel = fonte_pequena.render(
            f"Nível: +{pontuacao_nivel}",
            True,
            (255, 255, 255)
        )
        tela.blit(texto_nivel, (LARGURA - 300, 60))

        # Título
        texto_titulo = fonte_titulo.render("Forme a Palavra!", True, BRANCO)
        rect_titulo = texto_titulo.get_rect(center=(LARGURA // 2, 70))
        tela.blit(texto_titulo, rect_titulo)

        # Dica
        texto_dica = fonte_grande.render(f"Palavra: {self.palavra_correta}", True, COR_LETRA)
        rect_dica = texto_dica.get_rect(center=(LARGURA // 2, 150))
        tela.blit(texto_dica, rect_dica)

        # Letras disponíveis
        y_disponiveis = 250
        texto_disp = fonte_media.render("CLIQUE nas letras para formar:", True, BRANCO)
        tela.blit(texto_disp, (80, y_disponiveis))

        mouse_pos = pygame.mouse.get_pos()

        total_largura = len(self.letras_disponiveis) * 60
        x_inicio = (LARGURA - total_largura) // 2

        for i, letra in enumerate(self.letras_disponiveis):
            rect_letra = pygame.Rect(x_inicio + i * 60, y_disponiveis + 50, 55, 55)

            cor_fundo = COR_LETRA
            if rect_letra.collidepoint(mouse_pos):
                cor_fundo = (255, 235, 100)
                pygame.draw.rect(tela, BRANCO, rect_letra.inflate(10, 10), 3)

            pygame.draw.rect(tela, cor_fundo, rect_letra)
            pygame.draw.rect(tela, COR_LETRA_BORDA, rect_letra, 3)

            texto_letra = fonte_grande.render(letra, True, PRETO)
            rect_texto = texto_letra.get_rect(center=rect_letra.center)
            tela.blit(texto_letra, rect_texto)

        # Palavra formada
        y_formada = 400
        texto_form = fonte_media.render("Sua palavra:", True, BRANCO)
        tela.blit(texto_form, (80, y_formada))

        if self.palavra_formada:
            total_largura_formada = len(self.palavra_formada) * 60
            x_inicio_formada = (LARGURA - total_largura_formada) // 2
        else:
            x_inicio_formada = LARGURA // 2 - 30

        for i, letra in enumerate(self.palavra_formada):
            rect_letra = pygame.Rect(x_inicio_formada + i * 60, y_formada + 50, 55, 55)
            pygame.draw.rect(tela, VERDE_SUCESSO, rect_letra)
            pygame.draw.rect(tela, (39, 174, 96), rect_letra, 3)

            texto_letra = fonte_grande.render(letra, True, BRANCO)
            rect_texto = texto_letra.get_rect(center=rect_letra.center)
            tela.blit(texto_letra, rect_texto)

        if not self.palavra_formada:
            rect_vazio = pygame.Rect(x_inicio_formada, y_formada + 50, 55, 55)
            pygame.draw.rect(tela, (100, 100, 100), rect_vazio, 3, border_radius=5)

        # Instruções
        if not self.correto:
            texto_inst = fonte_pequena.render("BACKSPACE: apagar  |  ENTER: verificar", True, BRANCO)
            rect_inst = texto_inst.get_rect(center=(LARGURA // 2, 540))
            tela.blit(texto_inst, rect_inst)
        else:
            texto_inst = fonte_pequena.render("Pressione ENTER para continuar.", True, BRANCO)
            rect_inst = texto_inst.get_rect(center=(LARGURA // 2, 540))
            if pygame.time.get_ticks() % 1000 < 500:
                tela.blit(texto_inst, rect_inst)

        # Mensagem
        if self.mensagem:
            cor_msg = VERDE_SUCESSO if self.correto else VERMELHO_ERRO

            if self.correto:
                fundo_rect = pygame.Rect(0, 180, LARGURA, 100)
                fundo_surface = pygame.Surface((fundo_rect.width, fundo_rect.height))
                fundo_surface.fill(VERDE_SUCESSO)
                fundo_surface.set_alpha(230)
                tela.blit(fundo_surface, fundo_rect)

                texto_msg = fonte_titulo.render(self.mensagem, True, BRANCO)
                rect_msg = texto_msg.get_rect(center=(LARGURA // 2, 230))

                texto_sombra = fonte_titulo.render(self.mensagem, True, (0, 100, 0))
                rect_sombra = texto_sombra.get_rect(center=(LARGURA // 2 + 3, 233))
                tela.blit(texto_sombra, rect_sombra)

                tela.blit(texto_msg, rect_msg)
            else:
                texto_msg = fonte_grande.render(self.mensagem, True, cor_msg)
                rect_msg = texto_msg.get_rect(center=(LARGURA // 2, 200))
                tela.blit(texto_msg, rect_msg)

    
    def get_rect_letras_disponiveis(self):
        """Retorna lista de retângulos das letras disponíveis para clique"""
        y_disponiveis = 250
        total_largura = len(self.letras_disponiveis) * 60
        x_inicio = (LARGURA - total_largura) // 2
        
        rects = []
        for i in range(len(self.letras_disponiveis)):
            rect = pygame.Rect(x_inicio + i * 60, y_disponiveis + 50, 55, 55)
            rects.append(rect)
        
        return rects
