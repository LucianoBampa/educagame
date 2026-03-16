import pygame
import sys
from relatorio import RelatorioAluno
from config import (
    LARGURA, ALTURA, FPS,
    FACIL, MEDIO, DIFICIL
)
from nivel import Nivel
from tela_formacao import TelaFormacao
from telas import TelaMenu, TelaFim
from typing import Optional


# ─────────────────────────────────────────────────────────────────────────────
#  PALAVRAS POR NÍVEL
#  Grupo 1 → curtas  (3–4 letras)   → plataformas FÁCIL
#  Grupo 2 → médias  (5–7 letras)   → plataformas MÉDIO
#  Grupo 3 → longas  (8+ letras)    → plataformas DIFÍCIL
# ─────────────────────────────────────────────────────────────────────────────
PALAVRAS_NIVEL = {
    1: ["MALA", "PATO", "RIO", "SOL", "CEU",
        "MORA", "CASA", "PELO", "VOZ", "LUZ"],

    2: ["CHUVA", "FLOR", "LIVRO", "PEDRA", "TERRA",
        "AMIGO", "FESTA", "PORTA", "VERDE", "NOITE"],

    3: ["BORBOLETA", "CHOCOLATE", "ELEFANTE", "FLORESTA", "MONTANHA",
        "PRINCESA", "TARTARUGA", "UNIVERSO", "GIRASSOL", "BIBLIOTECA"],
}

DIFICULDADE_NIVEL = {1: FACIL, 2: MEDIO, 3: DIFICIL}

NIVEIS_INFO = {
    1: {"titulo": "NÍVEL 1", "subtitulo": "Palavras Curtas",
        "desc": "3 a 4 letras", "cor": (46, 204, 113)},
    2: {"titulo": "NÍVEL 2", "subtitulo": "Palavras Médias",
        "desc": "5 a 7 letras", "cor": (241, 196, 15)},
    3: {"titulo": "NÍVEL 3", "subtitulo": "Palavras Longas",
        "desc": "8+ letras",   "cor": (231, 76, 60)},
}


class Jogo:
    """Classe principal que gerencia o jogo"""

    def __init__(self):
        pygame.init()

        self.tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.NOFRAME)
        pygame.display.set_caption("Aventura das Letras")

        self.clock = pygame.time.Clock()

        self.fonte_titulo  = pygame.font.Font(None, 80)
        self.fonte_grande  = pygame.font.Font(None, 64)
        self.fonte_media   = pygame.font.Font(None, 48)
        self.fonte_pequena = pygame.font.Font(None, 32)

        self._reset_completo()

    # ─────────────────────────────────────────────────────────────────────────
    #  RESET
    # ─────────────────────────────────────────────────────────────────────────

    def _reset_completo(self):
        """Reinicia tudo — volta para tela de cadastro."""
        self.estado = "menu"

        # Cadastro
        self.ra_aluno        = ""
        self.nome_aluno      = ""
        self.turma_aluno     = ""
        self.digitando_ra    = True
        self.digitando_nome  = False
        self.digitando_turma = False

        # Seleção de nível
        self.nivel_selecionado = 1

        # Sessão atual
        self.nivel_grupo      = 1      # grupo escolhido pelo aluno (1, 2 ou 3)
        self.nivel_indice     = 0      # palavra atual dentro do grupo (0–9)
        self.dificuldade      = FACIL  # dificuldade da sessão atual
        self.palavras_jogadas = PALAVRAS_NIVEL[1]  # lista de palavras da sessão

        # Pontuação
        self.pontuacao_total = 0
        self.erros_totais    = 0
        self.acertos_totais  = 0
        self.tempo_inicio    = pygame.time.get_ticks()
        self.tempo_total     = 0

        self.nivel: Optional[Nivel] = None
        self.tela_formacao: Optional[TelaFormacao] = None

    # ─────────────────────────────────────────────────────────────────────────
    #  FLUXO DE JOGO
    # ─────────────────────────────────────────────────────────────────────────

    def _acumular_nivel(self):
        """Soma stats do nível atual nos contadores da sessão."""
        if self.nivel:
            self.pontuacao_total += self.nivel.pontuacao
            self.acertos_totais  += self.nivel.acertos
            self.erros_totais    += self.nivel.erros

    def iniciar_sessao(self):
        """Começa a sessão: define grupo escolhido e inicia 1ª palavra."""
        self.nivel_grupo      = self.nivel_selecionado
        self.nivel_indice     = 0
        self.dificuldade      = DIFICULDADE_NIVEL[self.nivel_grupo]
        self.palavras_jogadas = PALAVRAS_NIVEL[self.nivel_grupo]
        self.pontuacao_total  = 0
        self.erros_totais     = 0
        self.acertos_totais   = 0
        self.tempo_inicio     = pygame.time.get_ticks()
        self._iniciar_palavra()

    def _iniciar_palavra(self):
        """Cria o objeto Nivel para a palavra atual."""
        palavra    = self.palavras_jogadas[self.nivel_indice]
        self.nivel = Nivel(palavra, self.dificuldade, self.fonte_media)
        self.estado = "jogando"

    def proximo_nivel(self):
        """Avança para a próxima palavra ou finaliza a sessão."""
        self._acumular_nivel()
        self.nivel_indice += 1

        if self.nivel_indice >= len(self.palavras_jogadas):
            self._finalizar_sessao()
        else:
            self._iniciar_palavra()

    def _finalizar_sessao(self):
        """Envia relatório, atualiza API e vai para tela de fim."""
        self.tempo_total = (pygame.time.get_ticks() - self.tempo_inicio) // 1000

        RelatorioAluno.gerar(
            self.ra_aluno,
            self.nome_aluno,
            self.turma_aluno,
            self.palavras_jogadas,
            self.acertos_totais,
            self.erros_totais,
            self.pontuacao_total,
            self.tempo_total,
            self.dificuldade 
        )

        TelaFim.iniciar_serpentinas()
        self.estado = "fim"

    # ─────────────────────────────────────────────────────────────────────────
    #  EVENTOS
    # ─────────────────────────────────────────────────────────────────────────

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    return False

                # ── CADASTRO ─────────────────────────────────────────────
                if self.estado == "menu":

                    if evento.key == pygame.K_UP:
                        if self.digitando_nome:
                            self.digitando_nome = False
                            self.digitando_ra   = True
                        elif self.digitando_turma:
                            self.digitando_turma = False
                            self.digitando_nome  = True

                    elif evento.key == pygame.K_DOWN:
                        if self.digitando_ra and len(self.ra_aluno) >= 10:
                            self.digitando_ra   = False
                            self.digitando_nome = True
                        elif self.digitando_nome and len(self.nome_aluno) > 0:
                            self.digitando_nome  = False
                            self.digitando_turma = True

                    if self.digitando_ra:
                        if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and len(self.ra_aluno) >= 10:
                            self.digitando_ra   = False
                            self.digitando_nome = True
                        elif evento.key == pygame.K_BACKSPACE:
                            self.ra_aluno = self.ra_aluno[:-1]
                        elif evento.unicode.isdigit() and len(self.ra_aluno) < 10:
                            self.ra_aluno += evento.unicode

                    elif self.digitando_nome:
                        if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and len(self.nome_aluno) > 0:
                            self.digitando_nome  = False
                            self.digitando_turma = True
                        elif evento.key == pygame.K_BACKSPACE:
                            if len(self.nome_aluno) == 0:
                                self.digitando_nome = False
                                self.digitando_ra   = True
                            else:
                                self.nome_aluno = self.nome_aluno[:-1]
                        else:
                            c = evento.unicode
                            if len(self.nome_aluno) < 45:
                                if c.isalpha():
                                    self.nome_aluno += c.upper()
                                elif c == " " and self.nome_aluno and not self.nome_aluno.endswith(" "):
                                    self.nome_aluno += " "

                    elif self.digitando_turma:
                        if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and len(self.turma_aluno) == 2:
                            self.digitando_turma   = False
                            self.nivel_selecionado = 1
                            self.estado            = "selecionar_nivel"
                        elif evento.key == pygame.K_BACKSPACE:
                            if len(self.turma_aluno) == 0:
                                self.digitando_turma = False
                                self.digitando_nome  = True
                            else:
                                self.turma_aluno = self.turma_aluno[:-1]
                        else:
                            c = evento.unicode
                            if len(self.turma_aluno) == 0 and c.isdigit() and c != "0":
                                self.turma_aluno += c
                            elif len(self.turma_aluno) == 1 and c.isalpha():
                                self.turma_aluno += c.upper()

                # ── SELEÇÃO DE NÍVEL ──────────────────────────────────────
                elif self.estado == "selecionar_nivel":
                    if evento.key in (pygame.K_LEFT, pygame.K_UP):
                        self.nivel_selecionado = max(1, self.nivel_selecionado - 1)
                    elif evento.key in (pygame.K_RIGHT, pygame.K_DOWN):
                        self.nivel_selecionado = min(3, self.nivel_selecionado + 1)
                    elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        self.iniciar_sessao()
                    elif evento.key == pygame.K_BACKSPACE:
                        self.turma_aluno     = ""
                        self.digitando_turma = True
                        self.estado          = "menu"

                # ── JOGANDO ───────────────────────────────────────────────
                elif (
                    self.estado == "jogando"
                    and self.nivel is not None
                    and evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER)
                ):
                    if len(self.nivel.letras_coletadas) == len(self.nivel.palavra_alvo):
                        self.tela_formacao = TelaFormacao(
                            self.nivel.letras_coletadas,
                            self.nivel.palavra_alvo
                        )
                        self.estado = "formando"

                # ── FORMANDO ─────────────────────────────────────────────
                elif (
                    self.estado == "formando"
                    and self.tela_formacao is not None
                    and self.nivel is not None
                ):
                    if evento.key == pygame.K_BACKSPACE:
                        self.tela_formacao.remover_ultima()

                    elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if self.tela_formacao.correto:
                            self.nivel.acertos += 1
                            self.proximo_nivel()
                        elif len(self.tela_formacao.palavra_formada) > 0:
                            acertou = self.tela_formacao.verificar()
                            if not acertou:
                                self.nivel.erros += 1
                                penalidade = self.tela_formacao.tentativas * 5
                                self.nivel.pontuacao = max(0, self.nivel.pontuacao - penalidade)

                # ── FIM → volta para cadastro ─────────────────────────────
                elif self.estado == "fim" and evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self._reset_completo()

            # Clique nas letras disponíveis
            if (
                self.estado == "formando"
                and self.tela_formacao is not None
                and evento.type == pygame.MOUSEBUTTONDOWN
            ):
                mx, my = pygame.mouse.get_pos()
                for i, rect in enumerate(self.tela_formacao.get_rect_letras_disponiveis()):
                    if rect.collidepoint(mx, my):
                        self.tela_formacao.adicionar_letra(
                            self.tela_formacao.letras_disponiveis[i])
                        break

        return True

    # ─────────────────────────────────────────────────────────────────────────
    #  UPDATE
    # ─────────────────────────────────────────────────────────────────────────

    def atualizar(self):
        if self.estado == "jogando" and self.nivel is not None:
            self.nivel.update()

    # ─────────────────────────────────────────────────────────────────────────
    #  DESENHO
    # ─────────────────────────────────────────────────────────────────────────

    def desenhar(self):
        if self.estado == "menu":
            self._desenhar_menu()

        elif self.estado == "selecionar_nivel":
            self._desenhar_selecionar_nivel()

        elif self.estado == "jogando" and self.nivel is not None:
            self.nivel.desenhar(
                self.tela,
                self.fonte_pequena, self.fonte_media,
                self.fonte_grande, self.pontuacao_total
            )

        elif (
            self.estado == "formando"
            and self.tela_formacao is not None
            and self.nivel is not None
        ):
            self.tela_formacao.desenhar(
                self.tela,
                self.fonte_titulo, self.fonte_grande,
                self.fonte_media, self.fonte_pequena,
                self.pontuacao_total, self.nivel.pontuacao
            )

        elif self.estado == "fim":
            TelaFim.desenhar(
                self.tela,
                self.fonte_titulo, self.fonte_grande,
                self.fonte_media, self.fonte_pequena,
                self.nome_aluno,
                self.pontuacao_total,
                self.acertos_totais,
                self.erros_totais,
                self.tempo_total,
                len(self.palavras_jogadas)
            )

        pygame.display.flip()

    def _desenhar_menu(self):
        self.tela.fill((30, 30, 60))
        cx = LARGURA // 2

        titulo = self.fonte_titulo.render("AVENTURA DAS LETRAS", True, (255, 255, 0))
        self.tela.blit(titulo, (cx - titulo.get_width() // 2, 60))

        cor_ra    = (0, 255, 0) if self.digitando_ra    else (180, 180, 180)
        cor_nome  = (0, 255, 0) if self.digitando_nome  else (180, 180, 180)
        cor_turma = (0, 255, 0) if self.digitando_turma else (180, 180, 180)

        # RA
        t = self.fonte_media.render("Digite seu RA:", True, (255, 255, 255))
        self.tela.blit(t, (cx - t.get_width() // 2, 190))
        r = self.fonte_grande.render(
            self.ra_aluno + ("|" if self.digitando_ra else ""), True, cor_ra)
        self.tela.blit(r, (cx - r.get_width() // 2, 245))

        # Nome
        t = self.fonte_media.render("Digite seu nome:", True, (255, 255, 255))
        self.tela.blit(t, (cx - t.get_width() // 2, 340))
        r = self.fonte_grande.render(
            self.nome_aluno + ("|" if self.digitando_nome else ""), True, cor_nome)
        self.tela.blit(r, (cx - r.get_width() // 2, 390))

        # Turma
        t = self.fonte_media.render("Digite sua turma:", True, (255, 255, 255))
        self.tela.blit(t, (cx - t.get_width() // 2, 490))
        r = self.fonte_grande.render(
            self.turma_aluno + ("|" if self.digitando_turma else ""), True, cor_turma)
        self.tela.blit(r, (cx - r.get_width() // 2, 540))

    def _desenhar_selecionar_nivel(self):
        self.tela.fill((30, 30, 60))
        cx = LARGURA // 2

        titulo = self.fonte_titulo.render("AVENTURA DAS LETRAS", True, (255, 255, 0))
        self.tela.blit(titulo, (cx - titulo.get_width() // 2, 60))

        saudacao = self.fonte_media.render(
            f"Olá, {self.nome_aluno}! Escolha o nível:", True, (255, 255, 255))
        self.tela.blit(saudacao, (cx - saudacao.get_width() // 2, 170))

        card_w, card_h = 280, 220
        gap     = 40
        x_start = cx - (card_w * 3 + gap * 2) // 2
        y_card  = 260

        for n, info in NIVEIS_INFO.items():
            x           = x_start + (n - 1) * (card_w + gap)
            selecionado = (n == self.nivel_selecionado)

            if selecionado:
                pygame.draw.rect(self.tela, info["cor"],
                                 (x - 6, y_card - 6, card_w + 12, card_h + 12),
                                 border_radius=16)

            cor_fundo = (20, 20, 50) if selecionado else (50, 50, 90)
            pygame.draw.rect(self.tela, cor_fundo,
                             (x, y_card, card_w, card_h), border_radius=12)

            cor_borda = info["cor"] if selecionado else (100, 100, 140)
            pygame.draw.rect(self.tela, cor_borda,
                             (x, y_card, card_w, card_h), 3, border_radius=12)

            t = self.fonte_grande.render(info["titulo"], True, info["cor"])
            self.tela.blit(t, (x + card_w // 2 - t.get_width() // 2, y_card + 20))

            t = self.fonte_media.render(info["subtitulo"], True, (255, 255, 255))
            self.tela.blit(t, (x + card_w // 2 - t.get_width() // 2, y_card + 90))

            t = self.fonte_pequena.render(info["desc"], True, (180, 180, 220))
            self.tela.blit(t, (x + card_w // 2 - t.get_width() // 2, y_card + 145))

            if selecionado:
                t = self.fonte_pequena.render("▼ SELECIONADO", True, info["cor"])
                self.tela.blit(t, (x + card_w // 2 - t.get_width() // 2, y_card + 185))

        inst = self.fonte_pequena.render(
            "◄ ► para navegar   |   ENTER para confirmar   |   BACKSPACE para voltar",
            True, (160, 160, 200))
        self.tela.blit(inst, (cx - inst.get_width() // 2, ALTURA - 60))

    # ─────────────────────────────────────────────────────────────────────────
    #  LOOP PRINCIPAL
    # ─────────────────────────────────────────────────────────────────────────

    def executar(self):
        rodando = True
        while rodando:
            self.clock.tick(FPS)
            rodando = self.processar_eventos()
            self.atualizar()
            self.desenhar()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Jogo().executar()