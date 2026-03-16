# 🎮 Aventura das Letras

## Descrição do Projeto

Jogo educativo de plataforma desenvolvido em Python para crianças do ensino fundamental. O jogador coleta letras espalhadas pelo cenário e depois deve formar a palavra correta.

**Público-alvo:** Crianças de 6 a 10 anos (1º ao 5º ano)

**Objetivo educacional:** Reforçar alfabetização, reconhecimento de letras e formação de palavras.

---

## 🎯 Projeto de Extensão

Este jogo foi desenvolvido como projeto de extensão do curso de Sistemas de Informação (5º período) em parceria com o Colégio Barretos.

**Objetivos do projeto:**
- Desenvolver ferramenta educacional digital
- Aplicar conhecimentos de programação em contexto real
- Avaliar impacto pedagógico com alunos e professores
- Contribuir para o processo de alfabetização

---

## 🕹️ Como Jogar

### Controles:
- **Setas ← →**: Mover o personagem
- **ESPAÇO**: Pular
- **ENTER**: Avançar telas / Verificar palavra
- **BACKSPACE**: Apagar letra (na tela de formação)
- **MOUSE**: Clicar nas letras para formar palavra

### Mecânica:
1. Use as setas para mover o personagem pelas plataformas
2. Pule com ESPAÇO para alcançar as letras amarelas
3. Colete todas as letras da palavra
4. Pressione ENTER para ir à tela de formação
5. Clique nas letras para montar a palavra correta
6. Pressione ENTER para verificar
7. Se acertar, avança para o próximo nível!

---

## 💻 Instalação

### Pré-requisitos:
- Python 3.7 ou superior
- pip (gerenciador de pacotes do Python)

### Passo a passo:

1. **Clone ou baixe o projeto**
```bash
# Se estiver usando git
git clone [url-do-repositorio]
cd aventura-letras

# Ou simplesmente baixe os arquivos e abra o terminal na pasta
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

OU instale o Pygame diretamente:
```bash
pip install pygame
```

3. **Execute o jogo**
```bash
python aventura_letras.py
```

---

## 📁 Estrutura do Código

```
aventura_letras.py
├── Classe Jogador      # Personagem principal com física de plataforma
├── Classe Plataforma   # Plataformas do cenário
├── Classe Letra        # Letras coletáveis com animação
├── Classe Nivel        # Gerencia cada fase do jogo
├── Classe TelaFormacao # Tela onde forma a palavra
└── Classe Jogo         # Gerenciador principal (menu, níveis, etc)
```

---

## 🎨 Recursos Atuais

✅ **Mecânica de plataforma funcional**
- Movimento suave do personagem
- Física de pulo e gravidade
- Colisão com plataformas

✅ **Sistema de coleta**
- Letras flutuantes animadas
- Feedback visual ao coletar
- Contador de progresso

✅ **Formação de palavras**
- Interface interativa
- Clique nas letras para formar
- Verificação automática

✅ **Múltiplos níveis**
- 5 palavras diferentes
- Progressão de dificuldade
- Tela de conclusão

---

## 🚀 Próximas Melhorias Sugeridas

### Fase 1 - Visual e Audio:
- [ ] Sprites personalizados para o personagem
- [ ] Backgrounds temáticos
- [ ] Efeitos sonoros (coleta, pulo, acerto/erro)
- [ ] Música de fundo

### Fase 2 - Pedagogia:
- [ ] Dicas visuais (imagem da palavra)
- [ ] Narração em áudio das letras
- [ ] Níveis de dificuldade (fácil, médio, difícil)
- [ ] Banco de palavras expandido

### Fase 3 - Gamificação:
- [ ] Sistema de pontos/estrelas
- [ ] Tempo bônus
- [ ] Power-ups especiais
- [ ] Placar de recordes

### Fase 4 - Dados e Avaliação:
- [ ] Salvar progresso do aluno
- [ ] Registrar tentativas e acertos
- [ ] Relatório para professores
- [ ] Exportar dados em JSON

---

## 📊 Para o Projeto de Extensão

### Aplicação na Escola:

**Preparação:**
1. Instalar em computadores do laboratório
2. Criar tutorial visual para as crianças
3. Preparar questionário de avaliação

**Durante os Testes:**
1. Observar interação das crianças
2. Anotar dificuldades e facilidades
3. Registrar tempo de jogo
4. Tirar fotos (com autorização)

**Coleta de Dados:**
- Questionário para alunos (curtiu? difícil/fácil?)
- Entrevista com professores
- Métricas: taxa de acerto, tempo por nível
- Feedback sobre interface e jogabilidade

**Documentação:**
- Relatório de desenvolvimento
- Análise dos resultados
- Depoimentos
- Propostas de melhorias

---

## 🛠️ Personalizando o Jogo

### Adicionar novas palavras:

No arquivo `aventura_letras.py`, localize a linha:
```python
self.palavras = ["GATO", "BOLA", "CASA", "FLOR", "LIVRO"]
```

Adicione suas palavras:
```python
self.palavras = ["GATO", "BOLA", "CASA", "FLOR", "LIVRO", "ESCOLA", "AMIGO", "CARRO"]
```

### Mudar cores:

Edite as constantes no início do código:
```python
AZUL = (100, 150, 255)
VERDE = (100, 200, 100)
# etc...
```

### Ajustar dificuldade:

Física do personagem:
```python
self.forca_pulo = -15  # Aumentar = pula mais alto
self.velocidade_x = 5  # Aumentar = anda mais rápido
self.gravidade = 0.8   # Aumentar = cai mais rápido
```

---

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais como parte de um projeto de extensão universitária.

---

## 👥 Contato

Projeto desenvolvido por: [Seu Nome]
Curso: Sistemas de Informação - 5º Período
Instituição: [Sua Faculdade]
Email: [seu-email]

**Parceria:** Colégio Barretos - Ensino Fundamental

---

## 🙏 Agradecimentos

- Colégio Barretos pela parceria
- Professores e alunos participantes
- Orientador do projeto de extensão

---

**Versão:** 1.0 (Protótipo)
**Data:** Fevereiro 2026
