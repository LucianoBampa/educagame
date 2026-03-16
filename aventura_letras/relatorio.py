import os
import requests
from datetime import datetime


class RelatorioAluno:

    @staticmethod
    def gerar(ra_aluno, nome_aluno, turma_aluno, palavras,
              acertos_totais, erros_totais, pontuacao_total,
              tempo_total, dificuldade=None):

        minutos = tempo_total // 60
        segundos = tempo_total % 60
        tempo_formatado = f"{minutos:02d}:{segundos:02d}"

        total_tentativas = acertos_totais + erros_totais
        aproveitamento = int((acertos_totais / total_tentativas) * 100) if total_tentativas > 0 else 0

        data = datetime.now().strftime("%d/%m/%Y %H:%M")

        texto = f"""
=====================================
        RELATÓRIO DE DESEMPENHO
=====================================

Nome: {nome_aluno}
RA: {ra_aluno}
Turma: {turma_aluno}
Data: {data}
Dificuldade: {dificuldade if dificuldade else 'N/A'}
Palavras trabalhadas: {len(palavras)}
Acertos: {acertos_totais}
Erros: {erros_totais}
Aproveitamento: {aproveitamento}%
Tempo de Jogo: {tempo_formatado}
Pontuação final: {pontuacao_total} pontos

=====================================
"""
        print(texto)

        # Salva relatório em arquivo
        if not os.path.exists("relatorios"):
            os.makedirs("relatorios")

        nome_arquivo = f"relatorios/{nome_aluno}_{ra_aluno}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(texto)

        # Envia para API
        dados = {
            "ra":          ra_aluno,
            "nome":        nome_aluno,
            "ano":         datetime.now().year,
            "turma":       turma_aluno,
            "jogo":        "aventura_letras",
            "dificuldade": dificuldade.lower() if dificuldade else None,
            "palavra":     str(len(palavras)),
            "acertos":     acertos_totais,
            "erros":       erros_totais,
            "pontuacao":   pontuacao_total,
            "tempo_total": tempo_total            
        }

        try:
            resposta = requests.post(
                "http://127.0.0.1:8000/api/client/sessoes/",
                json=dados
            )
            print("Status envio API:", resposta.status_code)
        except Exception as erro:
            print("Erro ao enviar dados para API:", erro)

        return texto