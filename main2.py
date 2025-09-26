import os
import importlib
import sys

APPS_FOLDER = "apps"

# Garante que a pasta atual esteja no path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def carregar_apps():
    apps = {}
    for arquivo in os.listdir(APPS_FOLDER):
        if arquivo.endswith(".py") and arquivo != "__init__.py":
            nome_modulo = arquivo[:-3]
            try:
                modulo = importlib.import_module(f"{APPS_FOLDER}.{nome_modulo}")
                # Verifica se o módulo possui função run()
                if hasattr(modulo, "run"):
                    # Usa uma variável APP_NAME se definida, senão o nome do arquivo
                    nome_legivel = getattr(modulo, "APP_NAME", nome_modulo)
                    apps[nome_legivel] = modulo.run
            except Exception as e:
                print(f"Erro ao carregar {nome_modulo}: {e}")
    return apps

def menu():
    apps = carregar_apps()
    if not apps:
        print("Nenhuma aplicação encontrada na pasta 'apps'.")
        return

    while True:
        print("\n=== MENU DE APLICAÇÕES ===")
        for i, app_name in enumerate(apps.keys(), 1):
            print(f"{i} - {app_name}")
        print("0 - Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '0':
            print("Saindo...")
            break
        elif escolha.isdigit() and 1 <= int(escolha) <= len(apps):
            app_nome = list(apps.keys())[int(escolha)-1]
            print(f"\n>>> Executando: {app_nome}\n")
            apps[app_nome]()  # chama a função run()
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
1