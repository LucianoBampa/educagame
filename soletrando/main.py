import pygame
import random
import threading
import pyttsx3
import sys
import json
import os
import tempfile
import config
import interface
from relatorio import enviar_sessao

# ---------------------------------------------------------------------------
# Inicialização
# ---------------------------------------------------------------------------
pygame.init()
pygame.key.set_repeat(300, 50)
info_monitor    = pygame.display.Info()
largura_inicial = info_monitor.current_w
altura_inicial  = info_monitor.current_h - 50
tela = pygame.display.set_mode((largura_inicial, altura_inicial), pygame.RESIZABLE)
pygame.display.set_caption(config.TITULO)

# ---------------------------------------------------------------------------
# Voz
# ---------------------------------------------------------------------------
VOZ_ID_BRASILEIRA = None
temp_engine = pyttsx3.init()
vozes = list(temp_engine.getProperty('voices') or [])  # type: ignore
for voz in vozes:
    if "brazil" in voz.name.lower() or "pt-br" in voz.id.lower():
        VOZ_ID_BRASILEIRA = voz.id
        break
del temp_engine

# ---------------------------------------------------------------------------
# Fontes
# ---------------------------------------------------------------------------
fonte_grande  = pygame.font.Font(None, config.TAM_GRANDE)
fonte_media   = pygame.font.Font(None, config.TAM_MEDIO)
fonte_pequena = pygame.font.Font(None, config.TAM_PEQUENO)

# ---------------------------------------------------------------------------
# Palavras
# ---------------------------------------------------------------------------
LISTAS_PALAVRAS = {
    "FACIL":   ["GATO", "CASA", "BOLA", "SAPO", "MESA", "FOGO", "SOFA", "LAGO", "GELO", "PATO"],
    "MEDIO":   ["CADERNO", "ESCOLA", "BRINCAR", "JARDIM", "QUEIJO", "FOGUETE", "PIRULITO", "ABACAXI", "PROVA", "ESTRADA"],
    "DIFICIL": ["AQUIFERO", "PROGRAMACAO", "CHOCOLATE", "ASTRONAUTA", "PARALELEPIPEDO", "HIPOPOTAMO", "XICARA", "HIDROXIDO", "BIBLIOTECA", "ALCACHOFRA"],
}

lista_atual        = []
palavras_pendentes = []
falando_agora      = False

# ---------------------------------------------------------------------------
# Voz
# ---------------------------------------------------------------------------
def executar_fala(texto):
    global falando_agora
    try:
        falando_agora = True
        tts = pyttsx3.init()
        if VOZ_ID_BRASILEIRA:
            tts.setProperty('voice', VOZ_ID_BRASILEIRA)
        tts.setProperty('rate', 150)
        tts.say(texto)
        tts.runAndWait()
    except:
        pass
    finally:
        falando_agora = False

def falar_palavra(palavra):
    if falando_agora: return
    threading.Thread(target=executar_fala, args=(f"A palavra é: {palavra}",), daemon=True).start()

def falar_texto_livre(texto):
    if falando_agora: return
    threading.Thread(target=executar_fala, args=(texto,), daemon=True).start()

# ---------------------------------------------------------------------------
# Helpers de jogo
# ---------------------------------------------------------------------------
def novo_jogo():
    if not palavras_pendentes:
        return None, 0, ""
    palavra = random.choice(palavras_pendentes)
    palavras_pendentes.remove(palavra)
    return palavra, 0, ""

def reiniciar_tudo():
    global palavras_pendentes, lista_atual
    palavras_pendentes = lista_atual.copy()
    return novo_jogo()

# ---------------------------------------------------------------------------
# Lê contexto do launcher se disponível
# ---------------------------------------------------------------------------
def carregar_contexto_launcher():
    path = os.path.join(tempfile.gettempdir(), "sessao_context.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

# ---------------------------------------------------------------------------
# Loop principal
# ---------------------------------------------------------------------------
def main():
    global tela

    # Tenta carregar dados do launcher
    contexto = carregar_contexto_launcher()
    if contexto:
        nome_texto  = contexto.get("nome", "")
        ra_texto    = str(contexto.get("ra_aluno", ""))
        turma_id    = str(contexto.get("turma_id", ""))
        estado_jogo = "MENU"
        campo_ativo = None
        turma_texto = ""
    else:
        nome_texto  = ""
        ra_texto    = ""
        turma_texto = ""
        turma_id    = ""
        estado_jogo = "LOGIN"
        campo_ativo = "RA"

    rodando = True
    relogio = pygame.time.Clock()

    # Variáveis da partida
    palavra_alvo     = ""
    indice_atual     = 0
    msg_erro         = ""
    jogo_zerado      = False
    tempo_erro       = 0
    animacao_indice  = -1
    animacao_escala  = 1.0
    pontuacao        = 0
    nivel_atual      = ""

    # Métricas da sessão
    acertos_sessao       = 0
    erros_sessao         = 0
    erros_palavra        = 0
    tempo_inicio_palavra = 0
    tempo_inicio_sessao  = 0

    while rodando:
        largura_tela = tela.get_width()
        altura_tela  = tela.get_height()
        centro_x     = largura_tela // 2
        centro_y     = altura_tela  // 2

        rect_box_ra     = pygame.Rect(centro_x - 150, centro_y - 130, 300, 50)
        rect_box_nome   = pygame.Rect(centro_x - 150, centro_y - 30,  300, 50)
        rect_box_turma  = pygame.Rect(centro_x - 150, centro_y + 70,  300, 50)
        rect_btn_entrar = pygame.Rect(centro_x - 100, centro_y + 160, 200, 60)

        interface.desenhar_fundo(tela)
        mx, my = pygame.mouse.get_pos()
        clicou = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

            elif event.type == pygame.VIDEORESIZE:
                nw = max(event.w, config.LARGURA_MINIMA)
                nh = max(event.h, config.ALTURA_MINIMA)
                tela = pygame.display.set_mode((nw, nh), pygame.RESIZABLE)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicou = True
                    if estado_jogo == "LOGIN":
                        if rect_box_ra.collidepoint((mx, my)):    campo_ativo = "RA"
                        elif rect_box_nome.collidepoint((mx, my)): campo_ativo = "NOME"
                        elif rect_box_turma.collidepoint((mx, my)): campo_ativo = "TURMA"

            elif event.type == pygame.KEYDOWN:

                # ── LOGIN MANUAL ─────────────────────────────────────────
                if estado_jogo == "LOGIN":
                    if event.key == pygame.K_TAB:
                        if campo_ativo == "RA":      campo_ativo = "NOME"
                        elif campo_ativo == "NOME":  campo_ativo = "TURMA"
                        else:                        campo_ativo = "RA"

                    elif event.key == pygame.K_RETURN:
                        turma_valida = (
                            len(turma_texto) == 2
                            and turma_texto[0].isdigit()
                            and turma_texto[1].isalpha()
                        )
                        if ra_texto and nome_texto and turma_valida:
                            turma_id    = turma_texto
                            estado_jogo = "MENU"
                        else:
                            if not ra_texto:      campo_ativo = "RA"
                            elif not nome_texto:  campo_ativo = "NOME"
                            else:                 campo_ativo = "TURMA"

                    elif event.key == pygame.K_BACKSPACE:
                        if campo_ativo == "RA":      ra_texto    = ra_texto[:-1]
                        elif campo_ativo == "NOME":  nome_texto  = nome_texto[:-1]
                        elif campo_ativo == "TURMA": turma_texto = turma_texto[:-1]

                    else:
                        c = event.unicode
                        if campo_ativo == "RA":
                            if c.isnumeric() and len(ra_texto) < 10:
                                ra_texto += c
                        elif campo_ativo == "NOME":
                            if (c.isalpha() or c == " ") and len(nome_texto) < 45:
                                nome_texto += c.upper()
                        elif campo_ativo == "TURMA":
                            if len(turma_texto) == 0 and c.isdigit() and c != "0":
                                turma_texto += c
                            elif len(turma_texto) == 1 and c.isalpha():
                                turma_texto += c.upper()

                # ── JOGANDO ──────────────────────────────────────────────
                elif estado_jogo == "JOGANDO":
                    if event.key == pygame.K_ESCAPE:
                        estado_jogo = "MENU"

                    elif jogo_zerado:
                        if event.key == pygame.K_RETURN:
                            # Envia relatório ao concluir o nível
                            tempo_total = (pygame.time.get_ticks() - tempo_inicio_sessao) // 1000
                            enviar_sessao(
                                ra_texto, nome_texto, turma_id,
                                nivel_atual,
                                acertos_sessao, erros_sessao,
                                pontuacao, tempo_total,
                                len(LISTAS_PALAVRAS[nivel_atual])
                            )
                            falar_texto_livre(
                                f"Parabéns {nome_texto}! "
                                f"Você completou todas as palavras. "
                                f"Sua pontuação foi {pontuacao}."
                            )
                            estado_jogo    = "MENU"
                            jogo_zerado    = False
                            pontuacao      = 0
                            acertos_sessao = 0
                            erros_sessao   = 0

                    else:
                        if indice_atual == len(palavra_alvo) and event.key == pygame.K_RETURN:
                            proxima, i, msg = novo_jogo()
                            erros_palavra        = 0
                            tempo_inicio_palavra = pygame.time.get_ticks()

                            if proxima is None:
                                jogo_zerado  = True
                                palavra_alvo = ""
                            else:
                                palavra_alvo = proxima
                                indice_atual = 0
                                msg_erro     = ""
                                falar_palavra(palavra_alvo)

                        elif event.key == pygame.K_SPACE and not jogo_zerado:
                            falar_palavra(palavra_alvo)

                        elif event.unicode.isalpha() and indice_atual < len(palavra_alvo):
                            letra = event.unicode.upper()

                            if letra == palavra_alvo[indice_atual]:
                                animacao_indice = indice_atual
                                animacao_escala = 1.5
                                indice_atual   += 1
                                msg_erro        = ""

                                if indice_atual == len(palavra_alvo):
                                    acertos_sessao += 1
                                    tempo_palavra   = (pygame.time.get_ticks() - tempo_inicio_palavra) / 1000
                                    if erros_palavra == 0:  pontuacao += 2
                                    elif erros_palavra < 5: pontuacao += 1
                                    print(f"[LOG] {nome_texto} | RA: {ra_texto} | Palavra: {palavra_alvo} | Erros: {erros_palavra} | Tempo: {tempo_palavra:.2f}s")
                            else:
                                msg_erro      = f"Ops! '{letra}' não é a correta."
                                tempo_erro    = pygame.time.get_ticks()
                                erros_palavra += 1
                                erros_sessao  += 1

        # Animação
        if animacao_escala > 1.0:
            animacao_escala -= 0.05
        else:
            animacao_escala = 1.0
            animacao_indice = -1

        # ── DESENHO ──────────────────────────────────────────────────────

        if estado_jogo == "LOGIN":
            titulo = fonte_grande.render("IDENTIFICAÇÃO DO ALUNO", True, config.BRANCO_GIZ)
            tela.blit(titulo, titulo.get_rect(center=(centro_x, centro_y - 250)))

            COR_ATIVA  = (255, 215, 0)
            COR_INATIVA = (180, 170, 155)

            cor_ra    = COR_ATIVA  if campo_ativo == "RA"    else COR_INATIVA
            cor_nome  = COR_ATIVA  if campo_ativo == "NOME"  else COR_INATIVA
            cor_turma = COR_ATIVA  if campo_ativo == "TURMA" else COR_INATIVA

            cursor_ra    = "|" if campo_ativo == "RA"    and pygame.time.get_ticks() % 1000 < 500 else ""
            cursor_nome  = "|" if campo_ativo == "NOME"  and pygame.time.get_ticks() % 1000 < 500 else ""
            cursor_turma = "|" if campo_ativo == "TURMA" and pygame.time.get_ticks() % 1000 < 500 else ""

            # RA
            lbl = fonte_pequena.render("Digite seu RA (apenas números):", True, config.BRANCO_GIZ)
            tela.blit(lbl, lbl.get_rect(center=(centro_x, centro_y - 170)))
            val = fonte_media.render(ra_texto + cursor_ra, True, cor_ra)
            tela.blit(val, val.get_rect(center=(centro_x, centro_y - 130)))

            # Nome
            lbl = fonte_pequena.render("Digite seu nome:", True, config.BRANCO_GIZ)
            tela.blit(lbl, lbl.get_rect(center=(centro_x, centro_y - 70)))
            val = fonte_media.render(nome_texto + cursor_nome, True, cor_nome)
            tela.blit(val, val.get_rect(center=(centro_x, centro_y - 30)))

            # Turma
            lbl = fonte_pequena.render("Turma (ex: 3A):", True, config.BRANCO_GIZ)
            tela.blit(lbl, lbl.get_rect(center=(centro_x, centro_y + 40)))
            val = fonte_media.render(turma_texto + cursor_turma, True, cor_turma)
            tela.blit(val, val.get_rect(center=(centro_x, centro_y + 80)))

            # Instrução / ENTER
            turma_valida = (
                len(turma_texto) == 2
                and turma_texto[0].isdigit()
                and turma_texto[1].isalpha()
            )
            pode_entrar = bool(ra_texto and nome_texto and turma_valida)

            if pode_entrar:
                ini = fonte_pequena.render("Pressione ENTER para começar", True, COR_ATIVA)
                tela.blit(ini, ini.get_rect(center=(centro_x, centro_y + 160)))
            else:
                dica = fonte_pequena.render("TAB para navegar entre os campos", True, COR_INATIVA)
                tela.blit(dica, dica.get_rect(center=(centro_x, centro_y + 160)))

        elif estado_jogo == "MENU":
            saudacao = fonte_pequena.render(
                f"Olá, {nome_texto}!  RA: {ra_texto}  |  Turma: {turma_id}",
                True, config.BRANCO_GIZ)
            tela.blit(saudacao, saudacao.get_rect(center=(centro_x, 30)))

            titulo = fonte_grande.render("ESCOLHA A DIFICULDADE", True, config.BRANCO_GIZ)
            tela.blit(titulo, titulo.get_rect(center=(centro_x, centro_y - 120)))

            def criar_botao_menu(texto, pos_y, chave_nivel):
                nonlocal estado_jogo, palavra_alvo, indice_atual, msg_erro
                nonlocal jogo_zerado, pontuacao, erros_palavra, tempo_inicio_palavra
                nonlocal nivel_atual, acertos_sessao, erros_sessao, tempo_inicio_sessao
                global lista_atual, palavras_pendentes

                largura_btn, altura_btn = 250, 70
                rect_btn  = pygame.Rect(centro_x - largura_btn // 2, pos_y, largura_btn, altura_btn)
                hover     = rect_btn.collidepoint((mx, my))
                cor_atual = config.MARROM_CLARO if hover else config.MARROM_MADEIRA
                interface.desenhar_botao(tela, texto, fonte_media,
                                         rect_btn.x, rect_btn.y,
                                         largura_btn, altura_btn,
                                         cor_atual, config.BRANCO_GIZ)
                if hover and clicou:
                    lista_atual          = LISTAS_PALAVRAS[chave_nivel].copy()
                    palavra_alvo, indice_atual, msg_erro = reiniciar_tudo()
                    jogo_zerado          = False
                    estado_jogo          = "JOGANDO"
                    nivel_atual          = chave_nivel
                    pontuacao            = 0
                    acertos_sessao       = 0
                    erros_sessao         = 0
                    erros_palavra        = 0
                    tempo_inicio_palavra = pygame.time.get_ticks()
                    tempo_inicio_sessao  = pygame.time.get_ticks()
                    pygame.time.delay(300)
                    falar_palavra(palavra_alvo)

            criar_botao_menu("FÁCIL",   centro_y - 20,  "FACIL")
            criar_botao_menu("MÉDIO",   centro_y + 70,  "MEDIO")
            criar_botao_menu("DIFÍCIL", centro_y + 160, "DIFICIL")

        elif estado_jogo == "JOGANDO":
            instrucao = fonte_pequena.render(
                "ESPAÇO: Ouvir  |  ENTER: Próxima  |  ESC: Menu",
                True, config.BRANCO_GIZ)
            tela.blit(instrucao, (centro_x - instrucao.get_width() // 2, 30))

            txt_pontos = fonte_media.render(f"Pontos: {pontuacao}", True, config.BRANCO_GIZ)
            tela.blit(txt_pontos, (largura_tela - txt_pontos.get_width() - 30, 20))

            info_aluno = fonte_pequena.render(
                f"{nome_texto}  |  Turma: {turma_id}", True, config.BRANCO_GIZ)
            tela.blit(info_aluno, (20, 20))

            if jogo_zerado:
                rect_fim = pygame.Rect(0, 0, 620, 290)
                rect_fim.center = (centro_x, centro_y)
                pygame.draw.rect(tela, config.BRANCO_GIZ, rect_fim, border_radius=10)

                for surf, cy in [
                    (fonte_grande.render("NÍVEL CONCLUÍDO!", True, (34, 100, 60)), centro_y - 70),
                    (fonte_media.render(f"Pontuação: {pontuacao}", True, config.MARROM_MADEIRA), centro_y - 15),
                    (fonte_media.render(f"Acertos: {acertos_sessao}  |  Erros: {erros_sessao}", True, config.MARROM_MADEIRA), centro_y + 40),
                    (fonte_pequena.render("ENTER: Enviar relatório e escolher novo nível  |  ESC: Menu", True, config.CINZA), centro_y + 100),
                ]:
                    tela.blit(surf, surf.get_rect(center=(centro_x, cy)))

            else:
                largura_palavra_total = len(palavra_alvo) * 80
                inicio_x     = centro_x - (largura_palavra_total // 2)
                pos_y_letras = centro_y - 50

                for i, letra_correta in enumerate(palavra_alvo):
                    pos_x = inicio_x + (i * 80)
                    if i < indice_atual:
                        escala = animacao_escala if i == animacao_indice else 1.0
                        interface.desenhar_quadrado_letra(tela, fonte_grande, letra_correta, pos_x, pos_y_letras, escala)
                    else:
                        pygame.draw.rect(tela, (20, 50, 30), (pos_x, pos_y_letras, 70, 70), border_radius=5)
                        interface.desenhar_underline(tela, pos_x, pos_y_letras)

                if msg_erro and (pygame.time.get_ticks() - tempo_erro < 2000):
                    txt = fonte_media.render(msg_erro, True, config.VERMELHO_ERRO)
                    tela.blit(txt, txt.get_rect(center=(centro_x, altura_tela - 100)))

                if indice_atual == len(palavra_alvo):
                    txt = fonte_media.render("Muito Bem! Pressione ENTER.", True, config.BRANCO_GIZ)
                    tela.blit(txt, txt.get_rect(center=(centro_x, pos_y_letras - 100)))

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()