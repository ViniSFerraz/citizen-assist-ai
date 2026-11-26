from assistente import Assistente


def main():
    assistente = Assistente("Citizen Assist AI")
    print(f"=== {assistente.nome} - Descarte de resíduos em São Paulo ===")
    while True:
        print("\n[1] Fazer uma pergunta")
        print("[2] Procurar por categoria")
        print("[3] Relatório de uso")
        print("[4] Exportar CSV")
        print("[0] Sair")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            assistente.perguntar()
        elif opcao == "2":
            assistente.navegar()
        elif opcao == "3":
            assistente.relatorio()
        elif opcao == "4":
            assistente.exportar_csv()
        elif opcao == "0":
            print("Até mais!")
            break
        else:
            print("Opção inválida.")


main()
