import os
import threading
import json
from datetime import datetime
from io import BytesIO

import requests
import matplotlib.pyplot as plt

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.button import MDIconButton
from kivy.uix.image import Image as KivyImage
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock

# Importa o LineGraphWidget
from line_graph import LineGraphWidget
# Ajustando o tamanho da janela
Window.size = (720, 1080)

# Carregando automaticamente o arquivo KV correspondente
Builder.load_file("telas.kv")

# Classe da tela SplashScreen
class SplashScreen(Screen):
    pass

# Classe da tela SecondScreen
class SecondScreen(Screen):
    def update_data(self, dados_empresa):

        # Atualizar os widgets com os dados obtidos
        self.ids.simbolo_label.text = f"{dados_empresa['simbolo']}"
        self.ids.nome_label.text = f"{dados_empresa['nome_completo']}"
        self.ids.cotacao_label.text = f"R$ {dados_empresa['cotacao']}"
        self.ids.preco_anterior_label.text = f"Preço Anterior: R$ {dados_empresa['preco_anterior']}"
        self.ids.volume_label.text = f"Volume: {dados_empresa['volume']}"

        # Limpar widgets no layout de gráficos antes de adicionar um novo gráfico
        self.ids.graph_layout_2.clear_widgets()


        # Carregar a imagem diretamente do diretorio_logos
        logo_path = os.path.join('diretorio_logos', f"{dados_empresa['simbolo']}.png")
        self.ids.logo_image.source = logo_path

# Classe da tela ThirdScreen
class ThirdScreen(Screen):
    pass

# Classe para um layout personalizado que suporta centralização e escalonamento do gráfico
class CenteredGraphLayout(BoxLayout, ScrollView):
    def __init__(self, **kwargs):
        super(CenteredGraphLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))

# Classe principal da aplicação
class HealthApp(MDApp):
    def build(self):
    
        # Criando o gerenciador de telas
        self.sm = ScreenManager()
        
        # Adicionando as telas ao gerenciador
        self.splash_screen = SplashScreen(name='splash')
        self.second_screen = SecondScreen(name='second')
        self.sm.add_widget(self.splash_screen)
        self.sm.add_widget(self.second_screen)
        self.third_screen = ThirdScreen(name='third')
        self.sm.add_widget(self.third_screen)

        # Retorne o gerenciador de telas como interface da aplicação
        return self.sm

    def favoritos(self):

        self.sm.current = 'third'
        self.load_favorites()

    def load_favorites(self):
        try:
            with open('add.json', 'r', encoding='utf-8') as file:
                favorites_data = json.load(file)
        except FileNotFoundError:
            print("Erro: O arquivo 'add.json' não foi encontrado.")
            return

        # Limpar a lista existente na ThirdScreen
        self.third_screen.ids.lista_layout.clear_widgets()

        # Adicionar dados dos favoritos à ThirdScreen, evitando repetições
        added_symbols = set()  # Conjunto para rastrear os símbolos já adicionados
        for favorite in favorites_data:
            symbol = favorite['simbolo']
            # Verificar se o símbolo já foi adicionado
            if symbol not in added_symbols:
                # Adicione apenas se não estiver repetido
                added_symbols.add(symbol)
                # Crie um OneLineListItem para cada favorito
                list_item = OneLineListItem(text=f"{symbol} - {favorite['nome_completo']}")
                # Adicione a propriedade theme_text_color para definir a cor do texto
                list_item.theme_text_color = 'Custom'
                list_item.text_color = [1, 1, 1, 0.5]  # Branco em RGBA
                list_item.bind(on_release=self.show_favorite_details)  # Adicione um evento ao clicar no item
                # Adicione o OneLineListItem à lista_layout
                self.third_screen.ids.lista_layout.add_widget(list_item)  
    def show_favorite_details(self, instance):
        self.second_screen.ids.graph_layout_2.clear_widgets()

        # Lógica para mostrar detalhes do favorito quando clicado
        # Você pode acessar os dados do favorito usando instance.text ou de acordo com a estrutura de dados que você está usando
        print(f"Detalhes do favorito: {instance.text}")

        # Obtém o código da empresa a partir do texto do item da lista
        codigo_empresa = instance.text.split(' - ')[0]

        # Obtém os dados da empresa
        dados_empresa = self.obter_cotacao(codigo_empresa)

        if dados_empresa:
            # Acessa a segunda tela e atualiza os widgets com os dados obtidos
            self.sm.current = 'second'
            self.second_screen.update_data(dados_empresa)
            self.obter_cotacoes_por_dia(codigo_empresa)
            self.create_graph_widget(os.path.join(os.path.dirname(__file__), "historico", f"{codigo_empresa}.json"))

    def botao_add_clicado(self):
        # Adicione a lógica que deseja executar quando o botão for clicado
        dados_empresa = {
            "simbolo": self.second_screen.ids.simbolo_label.text,
            "nome_completo": self.second_screen.ids.nome_label.text,
            "cotacao": self.second_screen.ids.cotacao_label.text,
            "preco_anterior": self.second_screen.ids.preco_anterior_label.text,
            "volume": self.second_screen.ids.volume_label.text,
        }

        if dados_empresa:
            self.salvar_json(dados_empresa)
            self.show_add_message()  # Mostra a mensagem
            Clock.schedule_once(self.hide_add_message, 2)  # Oculta a mensagem após 2 segundos
            print("Informações salvas no arquivo add.json!")

   
    def show_add_message(self):
        # Exibe a mensagem na Tela 2
        self.second_screen.ids.aviso_label.text = "Empresa adicionada!"

    def hide_add_message(self, dt):
        # Oculta a mensagem na Tela 2
        self.second_screen.ids.aviso_label.text = ""
    
   
    
    def salvar_json(self, dados_empresa):
        # Salva as informações em um arquivo JSON
        arquivo_json = "add.json"
        try:
            with open(arquivo_json, "r", encoding="utf-8") as file:
                # Carrega o conteúdo atual do arquivo se existir
                data = json.load(file)
        except FileNotFoundError:
            # Cria um novo arquivo se não existir
            data = []

        # Adiciona os novos dados à lista
        data.append(dados_empresa)

        # Salva a lista no arquivo JSON
        with open(arquivo_json, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    def on_start(self):
        # Inicia a tarefa demorada em um thread secundário
        threading.Thread(target=self.perform_background_task).start()

        # Verifica se o arquivo de fonte existe antes de usá-lo
        font_path = "Poppins-SemiBold.ttf"
        if not os.path.exists(font_path):
            print(f"Erro: O arquivo de fonte '{font_path}' não foi encontrado.")
            return
    def obter_cotacao(self, code):
        # Construir a URL com o endpoint de cotação para um ticker específico
        url = f"https://brapi.dev/api/quote/{code}?token=4Rgd828GN7h8cLkUrxP1gK"

        # Fazer a solicitação HTTP
        response = requests.get(url)

        # Verificar o código de status da resposta
        if response.status_code == 200:
            # Se a solicitação foi bem-sucedida, imprimir a cotação se disponível
            dados = response.json()

            # Extração de dados
            cotacao = dados['results'][0]['regularMarketPrice']
            simbolo = dados['results'][0]['symbol']
            nome_completo = dados['results'][0]['longName']
            preco_anterior = dados['results'][0]['regularMarketPreviousClose']
            volume = dados['results'][0]['regularMarketVolume']

            # Imprimir dados
            print(f"Codigo: {simbolo}")
            print(f"Nome Completo: {nome_completo}")
            print(f"Cotação: {cotacao}")
            print(f"Preço Anterior: {preco_anterior}")
            print(f"Volume: {volume}")

            # Retornar os dados
            return {
                "simbolo": simbolo,
                "nome_completo": nome_completo,
                "cotacao": cotacao,
                "preco_anterior": preco_anterior,
                "volume": volume,
            }
        else:
            # Se houve um erro na solicitação, imprimir a mensagem de erro
            erro = response.json()
            print(f"Erro na solicitação: {erro['message']}")
            return None


    def perform_background_task(self):
        # Adicione sua lógica de tarefa de segundo plano aqui
        
        print("Background task is running.")
    def search_company(self, query):
          
        self.second_screen.ids.graph_layout_2.clear_widgets()
        # Carregue o JSON
        try:
            with open('empresas.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            print("Erro: O arquivo 'empresas.json' não foi encontrado.")
            return

        # Pesquise a empresa pelo nome ou código
        result = None
        for code, name in data.items():
            if query.lower() in name.lower() or query.lower() in code.lower():
                result = {"codigo": code, "nome": name}
                break
        if result:
            dados_empresa = self.obter_cotacao(result['codigo'])

            if dados_empresa:
                historico_folder = os.path.join(os.path.dirname(__file__), "historico")
                caminho = os.path.join(historico_folder, f"{result['codigo']}.json")

                # Limpar widgets antes de adicionar um novo gráfico
                self.second_screen.ids.graph_layout_2.clear_widgets()

                # Atualizar os widgets na SecondScreen
                self.sm.current = 'second'
                self.second_screen.update_data(dados_empresa)
                self.obter_cotacoes_por_dia(result['codigo'])

                # Limpar widgets antes de adicionar um novo gráfico
                self.second_screen.ids.graph_layout_2.clear_widgets()

                # Criar ou atualizar o gráfico
                self.create_graph_widget(caminho)

    def obter_cotacoes_por_dia(self, ticker):
        
        # Construir o caminho da pasta "historico"
        historico_folder = os.path.join(os.path.dirname(__file__), "historico")

        # Verificar se a pasta "historico" existe, caso contrário, criar
        if not os.path.exists(historico_folder):
            os.makedirs(historico_folder)

        # Construir o caminho completo para o arquivo na pasta "historico"
        nome_arquivo = os.path.join(historico_folder, f"{ticker}.json")

        # Construir a URL com o endpoint para obter as informações por dia
        url = f"https://brapi.dev/api/quote/{ticker}?range=3mo&interval=1d&token=4Rgd828GN7h8cLkUrxP1gK"

        try:
            # Fazer a solicitação HTTP
            response = requests.get(url)

            # Verificar o código de status da resposta
            print(f"Código de status: {response.status_code}")

            # Verificar se a solicitação foi bem-sucedida
            response.raise_for_status()

            # Obter os dados de cotação
            dados_cotacao = response.json().get('results', [])

            if dados_cotacao:
                self.second_screen.ids.graph_layout_2.clear_widgets()
                dados_formatados = {
                    'longName': dados_cotacao[0]['longName'],
                    'symbol': dados_cotacao[0]['symbol'],
                    'historicalDataPrice': dados_cotacao[0]['historicalDataPrice']
                }

                # Construa o caminho completo para o arquivo na pasta "historico"
                caminho = os.path.join(historico_folder, f"{ticker}.json")

                with open(caminho, 'w', encoding='utf-8') as json_file:
                    json.dump(dados_formatados, json_file, ensure_ascii=False, indent=4)
                    print(f"Dados formatados e salvos com sucesso em '{caminho}'.")
                
            else:
                print(f"Falha ao obter as cotações dos últimos 3 meses para {ticker}.")
        
        except requests.exceptions.HTTPError as errh:
            print(f"Erro HTTP: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Erro de conexão: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout na solicitação: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Erro na solicitação: {err}")
                       
    def create_graph_widget(self, caminho):
        # Carregue os dados do arquivo JSON
        with open(caminho, 'r') as file:
            json_data = json.load(file)

        # Extrair datas e preços de fechamento
        dates = [datetime.utcfromtimestamp(entry['date']).strftime('%Y-%m-%d') for entry in json_data['historicalDataPrice']]
        closes = [entry['close'] for entry in json_data['historicalDataPrice']]

        # Obtém as dimensões da janela
        window_width, window_height = Window.size

        # Define a proporção que você deseja para o gráfico (pode ser ajustada conforme necessário)
        graph_aspect_ratio = 20/ 9  # Exemplo: proporção 16:9

        # Calcula o tamanho proporcional do gráfico
        graph_width = window_width * 0.9
        graph_height = graph_width / graph_aspect_ratio

        # Atualiza o tamanho do layout e do widget de imagem
        self.second_screen.ids.graph_layout_2.size = (graph_width, graph_height)
        self.second_screen.ids.graph_layout_2.size_hint = (None, None)

        # Criar uma nova figura com eixo
        fig, ax = plt.subplots(figsize=(graph_width / 80, graph_height / 80))  # Ajuste de escala

        # Adicionar linhas de plotagem com marcadores e estilo de linha
        ax.plot(dates, closes, marker='s', linestyle='--', color='skyblue', label='Preço de Fechamento')

        # Adicionar grid ao gráfico
        ax.grid(True, linestyle='--', alpha=0.7)

        # Ajustar título e rótulos
        ax.set_title(f'Histórico de Preços para {" ".join(json_data["longName"].split()[:2])} (3 meses)', color='white', fontsize=22)
        ax.set_xlabel('Data', color='white', fontsize=12)
        ax.set_ylabel('Preço de Fechamento (R$)', color='white', fontsize=20)

        # Ajustar rótulos x para melhor legibilidade
        month_starts = [date for date in dates if date.endswith('-01')]
        ax.set_xticks(month_starts)

        # Configurações de cor para elementos do gráfico
        ax.tick_params(axis='x', rotation=45, colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.legend().get_texts()[0].set_color("white")

        # Ajustar cores de fundo do gráfico e da figura
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f'graph_{timestamp}.png'
        buffer = BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)

        # Criar widget de imagem Kivy e adicioná-lo ao layout
        img = CoreImage(BytesIO(buffer.read()), ext='png', filename=filename)
        image_widget = KivyImage(texture=img.texture, size=img.size, size_hint=(None, None))

        # Adicionar o widget de imagem ao layout, centralizando o gráfico
        self.second_screen.ids.graph_layout_2.clear_widgets()  # Limpar widgets antes de adicionar um novo gráfico
        self.second_screen.ids.graph_layout_2.add_widget(image_widget)
        self.second_screen.ids.graph_layout_2.size = img.size
        self.second_screen.ids.graph_layout_2.size_hint = (None, None)
    
# INICIA O APP
if __name__ == "__main__":
    HealthApp().run()