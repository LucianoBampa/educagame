import requests
SERVER = ""
class Tracker:
    def __init__(self, servidor=SERVER):
        self.servidor = servidor
        self.dados = []

    def registrar(self, evento: dict):
        self.dados.append(evento)

    def enviar(self):
        try:
            resposta = requests.post(
                f"{self.servidor}/endpoint",
                json=self.dados,
                timeout=5
            )

            if resposta.status_code == 200:
                print("Dados enviados com sucesso")
                self.dados.clear()
            else:
                print(f"Erro ao enviar: {resposta.status_code}")

        except requests.RequestException as e:
            print(f"Falha na conexão: {e}")



        

