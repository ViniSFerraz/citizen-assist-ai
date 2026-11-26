class Orientacao:
    def __init__(self, id, categoria, titulo, palavras_chave, resposta, fonte, acessos=0):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave
        self.resposta = resposta
        self.fonte = fonte
        self.acessos = acessos

    def exibir(self):
        print(f"\n>> {self.titulo} [{self.categoria}]")
        print(self.resposta)
        print(f"Fonte: {self.fonte}")
        print("Aviso: este assistente NÃO é um canal oficial.")
        self.registrar_acesso()

    def registrar_acesso(self):
        self.acessos += 1

    def adicionar_palavra_chave(self, palavra):
        if palavra in self.palavras_chave:
            return False
        self.palavras_chave.append(palavra)
        return True

    def para_dict(self):
        return {
            "id": self.id,
            "categoria": self.categoria,
            "titulo": self.titulo,
            "palavras_chave": self.palavras_chave,
            "resposta": self.resposta,
            "fonte": self.fonte,
            "acessos": self.acessos,
        }
