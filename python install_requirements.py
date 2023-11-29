import subprocess


required_packages = {
    'requests': '2.31.0',
    'matplotlib': '3.8.2',
    'kivy': '2.2.1',
    'kivymd': '1.1.1',
}

try:
    # Instalação dos pacotes com versões específicas
    for package, version in required_packages.items():
        subprocess.run(['pip', 'install', f'{package}=={version}'])
        
    # Exibir versões após a instalação
    subprocess.run(['pip', 'freeze'])

except Exception as e:
    print(f"Ocorreu um erro durante a instalação: {e}")
