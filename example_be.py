from py2neo import Graph, Node, Relationship

#                     |1 | 2 |          | 3 |
graph = Graph("http://gui:abc@127.0.0.1:7474/db/data")
# 1: username
# 2: password
# 3: port

def initialize():
    delete_query = """
        MATCH(n) DETACH DELETE n
    """
    graph.run(delete_query)

    graph.run("CREATE CONSTRAINT ON (d:Deputado) ASSERT d.nomeCivil is UNIQUE;")
    graph.run("CREATE CONSTRAINT ON (d:Deputado) ASSERT d.id is UNIQUE;")
    graph.run("CREATE CONSTRAINT ON (p:Partido) ASSERT p.sigla is UNIQUE;")
    graph.run("CREATE CONSTRAINT ON (m:Municipio) ASSERT m.nome is UNIQUE;")
    graph.run("CREATE CONSTRAINT ON (uf:UnidadeFederativa) ASSERT uf.sigla is UNIQUE;")


    get_ids_query = """
        WITH 'https://dadosabertos.camara.leg.br/api/v2/deputados?ordem=ASC&ordenarPor=nome' AS url
        CALL apoc.load.json(url) YIELD value
        UNWIND value.dados as dados
        RETURN dados.id
    """
    ids = [r['dados.id'] for r in graph.run(get_ids_query)]

    for id in ids:
        init_deputado_query = """
            WITH 'https://dadosabertos.camara.leg.br/api/v2/deputados/{id}'""".format(id=id) + """ AS url
            CALL apoc.load.json(url) YIELD value
            UNWIND value.dados as dados

            MERGE(d:Deputado {id : TOINT(dados.id), nomeCivil : dados.nomeCivil})
                ON CREATE SET d.idLegislatura = dados.ultimoStatus.idLegislatura, d.uri = dados.uri, d.urlFoto = dados.ultimoStatus.urlFoto,
                d.sexo = dados.sexo, d.nascimento = DATE(dados.dataNascimento), d.cpf = dados.cpf, d.email = dados.ultimoStatus.gabinete.email

            MERGE(p:Partido {sigla : dados.ultimoStatus.siglaPartido})

            MERGE (d)-[:FILIADO]-(p)

            FOREACH(t IN CASE WHEN dados.ufNascimento IS NOT NULL THEN [1] else [] END |
                MERGE(m:Municio {nome: dados.municipioNascimento})
                MERGE(uf: UnidadeFederativa {sigla: dados.ufNascimento})
                MERGE (d)-[:ORIGEM]->(m)
                MERGE (m)-[:SITUADO]-(uf)
            )		
        """
        graph.run(init_deputado_query)

def get_deputados():
    query = """
        MATCH(dep:Deputado)
        RETURN dep.Nome
    """

    deputados = []
    for record in graph.run(query):
        deputados.append(record["dep.Nome"])
    
    return deputados
