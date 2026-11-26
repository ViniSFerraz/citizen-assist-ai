import csv
from base_conhecimento import BaseConhecimento


class Assistente:
    def __init__(self, nome):
        self.nome = nome
        self.base = BaseConhecimento()

    def ler_numero(self, mensagem, maximo):
        while True:
            valor = input(mensagem).strip()
            if valor.isdigit() and 0 <= int(valor) <= maximo:
                return int(valor)
            print(f"Opção inválida. Digite um número de 0 a {maximo}.")

    def sim_ou_nao(self, mensagem):
        while True:
            valor = input(mensagem).strip().lower()
            if valor in ("s", "n"):
                return valor == "s"
            print("Responda apenas s ou n.")

    def tem_dado_pessoal(self, texto):
        digitos = 0
        for c in texto:
            if c.isdigit():
                digitos += 1
        return digitos >= 8 or "@" in texto

    def mostrar(self, orientacao):
        orientacao.exibir()
        self.base.salvar()

    def perguntar(self):
        pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()
        if pergunta == "0":
            return
        if pergunta == "":
            print("Você não digitou nada.")
            return
        if self.tem_dado_pessoal(pergunta):
            print("Não digite CPF, telefone, e-mail ou outros dados pessoais. Pergunta recusada.")
            return

        resultado = self.base.buscar(pergunta)
        if len(resultado) == 0 or resultado[0][0] < 3:
            print("Não encontrei uma orientação confiável para essa dúvida.")
            if self.sim_ou_nao("Quer procurar pelas categorias? (s/n): "):
                self.navegar(pergunta)
            return

        pontos, orientacao = resultado[0]
        if pontos >= 6:
            print(f"\nConfiança ALTA ({pontos} pontos)")
        else:
            print(f"\nConfiança MÉDIA ({pontos} pontos)")
        self.mostrar(orientacao)

        if not self.sim_ou_nao("Essa orientação respondeu sua dúvida? (s/n): "):
            if self.sim_ou_nao("Quer procurar pelas categorias? (s/n): "):
                self.navegar(pergunta)

    def navegar(self, pergunta=""):
        categorias = self.base.categorias()
        linha = ""
        for i, c in enumerate(categorias, 1):
            linha += f"[{i}] {c} "
        print(linha)
        n = self.ler_numero("Escolha a categoria (0 para voltar): ", len(categorias))
        if n == 0:
            return

        lista = [o for o in self.base.orientacoes if o.categoria == categorias[n - 1]]
        for i, o in enumerate(lista, 1):
            print(f"[{i}] {o.titulo}")
        n = self.ler_numero("Escolha a orientação (0 para voltar): ", len(lista))
        if n == 0:
            return

        orientacao = lista[n - 1]
        self.mostrar(orientacao)
        if pergunta != "" and self.sim_ou_nao("Essa orientação respondeu sua dúvida? (s/n): "):
            self.aprender(pergunta, orientacao)

    def aprender(self, pergunta, orientacao):
        candidatas = self.base.palavras_novas(pergunta, orientacao)
        if len(candidatas) == 0:
            print("Não tem palavra nova para aprender nessa pergunta.")
            return
        aprendidas = 0
        for palavra in candidatas:
            if self.sim_ou_nao(f"Aprender '{palavra}' para '{orientacao.titulo}'? (s/n): "):
                if orientacao.adicionar_palavra_chave(palavra):
                    aprendidas += 1
        if aprendidas > 0:
            self.base.salvar()
        print(f"{aprendidas} palavra(s)-chave aprendida(s).")

    def relatorio(self):
        print("\n=== Relatório de uso ===")
        print("3 orientações mais acessadas:")
        for o in self.base.ranking()[:3]:
            print(f"  {o.titulo}: {o.acessos} acesso(s)")

        print("Nunca acessadas:")
        nunca = [o for o in self.base.orientacoes if o.acessos == 0]
        if len(nunca) == 0:
            print("  nenhuma")
        for o in nunca:
            print(f"  {o.titulo}")

        por_categoria = {}
        for o in self.base.orientacoes:
            por_categoria[o.categoria] = por_categoria.get(o.categoria, 0) + o.acessos
        print("Total de acessos por categoria:")
        for categoria, total in por_categoria.items():
            print(f"  {categoria}: {total}")

    def exportar_csv(self):
        campos = ["id", "categoria", "titulo", "acessos", "total_palavras_chave"]
        with open("data/relatorio.csv", "w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=campos)
            escritor.writeheader()
            for o in self.base.orientacoes:
                escritor.writerow({
                    "id": o.id,
                    "categoria": o.categoria,
                    "titulo": o.titulo,
                    "acessos": o.acessos,
                    "total_palavras_chave": len(o.palavras_chave),
                })
        print("Relatório exportado em data/relatorio.csv")
