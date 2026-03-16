var altura = 0
var largura = 0
var vidas = 0
var MaxVidas = 5
var tempo = 60

var mosquitosCapturados = 0
var pontuacaoFinal = 0

var criaMosquitoTempo = 2000

var nivel = window.location.search
nivel = nivel.replace('?', '')

if (nivel === 'facil') {
	criaMosquitoTempo = 3000
} else if (nivel === 'normal') {
	criaMosquitoTempo = 2000
} else if (nivel === 'dificil') {
	criaMosquitoTempo = 1300
} else if (nivel === 'muito_dificil') {
	criaMosquitoTempo = 900
}

function ajustaTamanhoPalcoJogo() {
	altura = window.innerHeight
	largura = window.innerWidth
}

ajustaTamanhoPalcoJogo()

var tempoInicial = new Date()

var cronometro = setInterval(async function () {

	tempo -= 1

	if (tempo < 0) {

		clearInterval(cronometro)
		clearInterval(criaMosquito)

		pontuacaoFinal = mosquitosCapturados * 10

		await gerarRelatorio()

		window.location.href = 'vitoria.html'

	} else {
		document.getElementById('cronometro').innerHTML = tempo
	}

}, 1000)

function posicaoRandomica() {

	if (document.getElementById('mosquito')) {

		document.getElementById('mosquito').remove()
		vidas++

		if (vidas >= MaxVidas) {

			pontuacaoFinal = mosquitosCapturados * 10

			gerarRelatorio().then(() => {
				window.location.href = 'fim_de_jogo.html'
			})

			return

		} else {
			document.getElementById('v' + vidas).src = "imagens/coracao_vazio.png"
		}
	}

	var posicaoX = Math.floor(Math.random() * largura) - 90
	var posicaoY = Math.floor(Math.random() * altura) - 90

	posicaoX = posicaoX < 0 ? 0 : posicaoX
	posicaoY = posicaoY < 0 ? 0 : posicaoY

	var mosquito = document.createElement('img')
	mosquito.src = 'imagens/mosquito.png'
	mosquito.className = tamanhoAleatorio() + ' ' + ladoAleatorio()
	mosquito.style.left = posicaoX + 'px'
	mosquito.style.top = posicaoY + 'px'
	mosquito.style.position = 'absolute'
	mosquito.id = 'mosquito'

	mosquito.onclick = function () {
		mosquitosCapturados++
		this.remove()
	}

	document.body.appendChild(mosquito)
}

function tamanhoAleatorio() {
	var classe = Math.floor(Math.random() * 3)
	switch (classe) {
		case 0: return 'mosquito1'
		case 1: return 'mosquito2'
		case 2: return 'mosquito3'
	}
}

function ladoAleatorio() {
	var classe = Math.floor(Math.random() * 2)
	switch (classe) {
		case 0: return 'ladoA'
		case 1: return 'ladoB'
	}
}

async function gerarRelatorio() {

	let tempoTotal = Math.floor((new Date() - tempoInicial) / 1000)

	let minutos = Math.floor(tempoTotal / 60)
	let segundos = tempoTotal % 60
	let tempoFormatado = String(minutos).padStart(2, '0') + ":" + String(segundos).padStart(2, '0')

	let relatorio = `
=====================================
        RELATÓRIO DE DESEMPENHO
=====================================
Aluno: ${localStorage.getItem("Nome")}
RA: ${localStorage.getItem("ra")}
Turma: ${localStorage.getItem("turma")}
Data: ${new Date().toLocaleString()}
Mosquitos capturados: ${mosquitosCapturados}
Dificuldade: ${nivel.toUpperCase()}
Tempo de Jogo: ${tempoFormatado}
Erros (vidas perdidas): ${vidas}
Pontuação final: ${pontuacaoFinal} pontos
=====================================`

	console.log(relatorio)

	await enviarRelatorioAPI(tempoTotal)
}

async function enviarRelatorioAPI(tempoTotal) {

	let dados = {
		nome: localStorage.getItem("nome"),
		ra: localStorage.getItem("ra"),
		turma: localStorage.getItem("turma"),
		jogo: "mata_mosquito",
		dificuldade: nivel,
		acertos: mosquitosCapturados,
		erros: vidas,
		pontuacao: pontuacaoFinal,
		tempo_total: tempoTotal,
	}

	try {
		let res = await fetch("http://127.0.0.1:8000/api/client/sessoes/", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify(dados)
		})
		if (!res.ok) {
			console.log("Erro HTTP:", res.status)
			return
		}

		let data = await res.json()

		console.log("Relatório enviado:", data)

	} catch (erro) {

		console.log("Erro ao enviar relatório:", erro)

	}

}