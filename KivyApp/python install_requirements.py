import os
import subprocess
import venv  # Importa o módulo venv

def create_venv(venv_dir='venv'):
    """
    Cria um ambiente virtual no diretório especificado.

    Parameters:
    - venv_dir: Diretório para criar o ambiente virtual.
    """
    subprocess.run(['python', '-m', 'venv', venv_dir], check=True)

def activate_venv(venv_dir='venv'):
    """
    Ativa o ambiente virtual.

    Parameters:
    - venv_dir: Diretório do ambiente virtual.
    """
    activate_script = os.path.join(venv_dir, 'Scripts', 'activate')
    subprocess.run([activate_script], check=True, shell=True)

def install_package(package, failed_packages):
    """
    Tenta instalar um pacote usando o pip.

    Parameters:
    - package: Nome do pacote a ser instalado.
    - failed_packages: Lista para armazenar pacotes que não puderam ser instalados.
    """
    try:
        subprocess.check_call(['pip', 'install', package])
        print(f"O pacote {package} foi instalado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao instalar {package}: {e}")
        print("Continuando com o próximo pacote...")
        failed_packages.append(package)

def install_requirements(file_path=None):
    """
    Instala os pacotes listados no arquivo requirements.txt.

    Parameters:
    - file_path: Caminho para o arquivo requirements.txt.
    """
    if file_path is None:
        file_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')

    with open(file_path, 'r') as file:
        packages = file.read().splitlines()

    failed_packages = []

    for package in packages:
        install_package(package, failed_packages)

    # Salva os pacotes que falharam em um arquivo
    with open('failed_packages.txt', 'w') as failed_file:
        for failed_package in failed_packages:
            failed_file.write(f"{failed_package}\n")

    if failed_packages:
        print("Pacotes que falharam na instalação:")
        for failed_package in failed_packages:
            print(f"- {failed_package}")

if __name__ == "__main__":
    # Cria e ativa o ambiente virtual
    create_venv()
    activate_venv()

    # Instala os requisitos do requirements.txt
    install_requirements()
