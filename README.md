YOUFIN é uma aplicação Kivy/Python para acompanhar informações financeiras de empresas. 
A aplicação possui uma interface gráfica interativa e permite visualizar dados de cotação em tempo real, histórico de preços e adicionar empresas aos favoritos.

Requisitos de Instalação
Antes de executar a aplicação, certifique-se de ter os requisitos necessários instalados. Execute o seguinte comando no terminal para instalar as dependências:


python install_requirements.py

Este comando instalará automaticamente os pacotes necessários, como requests, matplotlib, kivy e kivymd.

Executando o Aplicativo
Após instalar os requisitos, você pode executar o aplicativo com o seguinte comando:


python main.py

Isso iniciará o aplicativo e abrirá a tela inicial. Você pode explorar as funcionalidades, pesquisar empresas, visualizar informações detalhadas e adicionar empresas aos favoritos.

Estrutura do Código Fonte
main.py: Arquivo principal que inicia o aplicativo.
install_requirements.py: Script para instalar automaticamente os requisitos do aplicativo.
line_graph.py: Módulo contendo a classe LineGraphWidget para exibir gráficos de linha.
telas.kv: Arquivo de layout Kivy contendo a estrutura da interface gráfica.
diretorio_logos/: Pasta contendo os logos das empresas.
historico/: Pasta para armazenar dados históricos de empresas.


Funcionalidades Principais
Pesquisar Empresas: Utilize a barra de pesquisa para encontrar informações sobre uma empresa específica.

Visualizar Detalhes: Ao clicar em uma empresa na lista de resultados, você pode visualizar detalhes, incluindo cotação, preço anterior e volume.

Histórico de Preços: Acesse o histórico de preços de uma empresa nos últimos 3 meses.

Adicionar aos Favoritos: Adicione empresas aos favoritos para acesso rápido.

Visualizar Favoritos: Acesse a lista de empresas favoritas para fácil referência.

Observações
Certifique-se de ter uma conexão de internet ativa para obter dados em tempo real.
Os dados históricos são salvos localmente para uma visualização mais rápida.
Consulte o arquivo install_requirements.py para garantir que todas as dependências estejam instaladas corretamente.
