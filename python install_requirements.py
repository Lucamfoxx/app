import subprocess

# Lista de pacotes necessários
required_packages = [
    'requests',
    'matplotlib',
    'kivy',
    'kivymd',
]

# Instalação dos pacotes
for package in required_packages:
    subprocess.run(['pip', 'install', package])

print("Todos os pacotes foram instalados com sucesso.")
