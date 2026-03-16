import os
import requests
from datetime import datetime


def enviar_sessao(ra, nome, turma, nivel, acertos, erros, pontuacao, tempo_total, palavras_trabalhadas):
    """Envia resultado da sessão para a API e imprime relatório no console."""

    minutos = tempo_total // 60
    segundos = tempo_total % 60
    total = acertos + erros
    aproveitamento = int((acertos / total) * 100) if total > 0 else 0
    data = datetime.now().strftime("%d/%m/%Y %H:%M")

    texto = f"""
=====================================
        RELATÓRIO DE DESEMPENHO
=====================================
Nome:   {nome}
RA:     {ra}
Turma:  {turma}
Data:   {data}
Nível:  {nivel}

Palavras trabalhadas: {palavras_trabalhadas}
Acertos:  {acertos}
Erros:    {erros}
Aproveitamento: {aproveitamento}%
Tempo de Jogo: {minutos:02d}:{segundos:02d}
Pontuação final: {pontuacao} pontos
=====================================
"""
    print(texto)

    # Envia para API
    dados = {
        "ra":          ra,
        "nome":        nome,
        "ano":         datetime.now().year,
        "turma":       str(turma),
        "jogo":        "soletrando",
        "dificuldade": nivel.lower(),
        "palavra":     str(palavras_trabalhadas),  # quantidade de palavras trabalhadas
        "acertos":     acertos,
        "erros":       erros,
        "pontuacao":   pontuacao,
        "tempo_total": tempo_total,
    }

    try:
        resposta = requests.post(
            "http://127.0.0.1:8000/api/client/sessoes/",
            json=dados,
            timeout=5
        )
        print(f"Status envio API: {resposta.status_code}")
    except Exception as e:
        print(f"Erro ao enviar para API: {e}")