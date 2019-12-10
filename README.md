# Câmara dos Deputados - Graph Network

## Requisitos mínimos
Ter instalado no sistema:
* Python 3
* Flask
* Neo4j
* Plugin APOC no Neo4j

## Passos para a execução

- Abrir o Neo4j
- Criar um novo projeto no Neo4j
- Criar um Grafo neste projeto
- Dar um "START" no grafo criado
- Utilizar o comando `python3 front_end.py` no terminal a partir da pasta onde esteja o arquivo `front_end.py`

Este comando irá chamar o `back_end.py` que irá criar o grafo (isto pode levar alguns minutos) e depois disponibilizará o link para acesso ao site local. Por default este deverá ser `http://localhost:7474/`.

Após a inicialização pode-se comentar a linha de inicialização do banco de dados (`camaraDosDeputados.init_db()`) necessária apenas para a primeira criação ou para futuras atualizações do Banco de Dados. Essa linha é encontrada no código no arquivo `front_end.py`.

