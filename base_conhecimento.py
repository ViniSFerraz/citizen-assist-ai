import json
from orientacao import Orientacao

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}

PALAVRAS_IGNORADAS = ("como", "onde", "quero", "preciso", "para", "posso", "pode",
                      "qual", "quais", "quando", "fazer", "levar", "levo", "jogar",
                      "jogo", "deixo", "deixar", "descartar", "descarte", "minha",
                      "meus", "minhas", "esse", "essa", "isso", "tenho", "uma", "umas")


def normalizar(texto):
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    def __init__(self, arquivo="data/base_conhecimento.json", arquivo_sinonimos="data/sinonimos.json"):
        self.arquivo = arquivo
        self.arquivo_sinonimos = arquivo_sinonimos
        self.orientacoes = []
        self.sinonimos = {}
        self.carregar()

    def carregar(self):
        try:
            with open(self.arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
            with open(self.arquivo_sinonimos, "r", encoding="utf-8") as f:
                self.sinonimos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Erro ao ler os arquivos da pasta data.")
            return
        for d in dados:
            self.orientacoes.append(Orientacao(d["id"], d["categoria"], d["titulo"], d["palavras_chave"],
                                               d["resposta"], d["fonte"], d["acessos"]))

    def salvar(self):
        lista = [o.para_dict() for o in self.orientacoes]
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(lista, f, ensure_ascii=False, indent=4)

    def pontuar(self, pergunta, orientacao):
        pontos = 0
        palavras = pergunta.split()
        for chave in orientacao.palavras_chave:
            if " " + chave + " " in pergunta:
                pontos += 3
        for palavra in palavras:
            for sinonimo in self.sinonimos.get(palavra, []):
                if sinonimo in orientacao.palavras_chave:
                    pontos += 2
        titulo = normalizar(orientacao.titulo).split()
        for palavra in palavras:
            if len(palavra) >= 4 and palavra in titulo:
                pontos += 1
        return pontos

    def buscar(self, pergunta):
        pergunta = normalizar(pergunta)
        resultado = []
        for o in self.orientacoes:
            pontos = self.pontuar(pergunta, o)
            if pontos > 0:
                resultado.append((pontos, o))
        resultado.sort(key=lambda item: item[0], reverse=True)
        return resultado

    def palavras_novas(self, pergunta, orientacao):
        novas = []
        for palavra in normalizar(pergunta).split():
            if len(palavra) < 4 or palavra in PALAVRAS_IGNORADAS:
                continue
            if palavra in orientacao.palavras_chave or palavra in novas:
                continue
            novas.append(palavra)
        return novas[:3]

    def ranking(self):
        return sorted(self.orientacoes, key=lambda o: o.acessos, reverse=True)

    def categorias(self):
        lista = []
        for o in self.orientacoes:
            if o.categoria not in lista:
                lista.append(o.categoria)
        return lista
