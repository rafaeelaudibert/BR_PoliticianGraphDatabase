from py2neo import Graph, Node, Relationship

#                     |1 | 2 |          | 3 |
graph = Graph("http://gui:abc@127.0.0.1:7474/db/data")
# 1: username
# 2: password
# 3: port

def initialize():
    graph.run("MATCH(n) DETACH DELETE n") # Clean database

    # Constraints : TODO Adicionar indexes
    graph.run("CREATE CONSTRAINT ON (d:Deputado) ASSERT d.nomeCivil is UNIQUE;")
    graph.run("CREATE CONSTRAINT ON (d:Deputado) ASSERT d.id is UNIQUE;")
    graph.run("CREATE CONSTRAINT ON (p:Partido) ASSERT p.sigla is UNIQUE;")
    graph.run("CREATE CONSTRAINT ON (m:Municipio) ASSERT m.nome is UNIQUE;")
    graph.run("CREATE CONSTRAINT ON (uf:UnidadeFederativa) ASSERT uf.sigla is UNIQUE;")

    get_depIds_query = """
        WITH 'https://dadosabertos.camara.leg.br/api/v2/deputados?ordem=ASC&ordenarPor=nome' AS url
        CALL apoc.load.json(url) YIELD value
        UNWIND value.dados as dados
        RETURN dados.id
    """
    depIds = [r['dados.id'] for r in graph.run(get_depIds_query)]

    for id in depIds:
        init_deputado_query = """
            WITH 'https://dadosabertos.camara.leg.br/api/v2/deputados/{id}'""".format(id=id) + """ AS url
            CALL apoc.load.json(url) YIELD value
            UNWIND value.dados as dados

            MERGE(d:Deputado {id : TOINT(dados.id), nomeCivil : dados.nomeCivil})
                ON CREATE SET d.nome = dados.ultimoStatus.nome, d.idLegislatura = dados.ultimoStatus.idLegislatura, d.uri = dados.uri, d.urlFoto = dados.ultimoStatus.urlFoto,
                d.sexo = dados.sexo, d.nascimento = DATE(dados.dataNascimento), d.cpf = dados.cpf, d.email = dados.ultimoStatus.gabinete.email, d.escolaridade = dados.escolaridade

            MERGE(p:Partido {sigla : dados.ultimoStatus.siglaPartido})
                ON CREATE SET p.uri = dados.ultimoStatus.uriPartido

            MERGE (d)-[:FILIADO]-(p)

            FOREACH(t IN CASE WHEN dados.ufNascimento IS NOT NULL THEN [1] else [] END |
                MERGE(m:Municio {nome: dados.municipioNascimento})
                MERGE(uf: UnidadeFederativa {sigla: dados.ufNascimento})
                MERGE (d)-[:ORIGEM]->(m)
                MERGE (m)-[:SITUADO]-(uf)
            )		
        """
        graph.run(init_deputado_query)

    for id in depIds:
        init_despesas_query = """
            WITH 'https://dadosabertos.camara.leg.br/api/v2/deputados/{id}/despesas?ano=2019&itens=100000&ordem=ASC&ordenarPor=mes'""".format(id=id) + """ AS url
            CALL apoc.load.json(url) YIELD value
            UNWIND value.dados as despesas
            """ + "MATCH (dep:Deputado {id:" +str(id) +"})" + """
            FOREACH(dados in despesas | 
                MERGE (t:TipoDespesa {tipo: dados.tipoDespesa})
                CREATE (des:Despesa {valorDocumento: dados.valorDocumento, codDocumento: dados.codDocumento, nomeFornecedor: dados.nomeFornecedor, urlDocumento: dados.urlDocumento, tipo: dados.tipoDocumento})
                CREATE (des)-[:TIPODESPESA]->(t)
                CREATE (dep)-[:GASTOU {data: DATE(dados.dataDocumento)}]->(des)
            )
        """
        graph.run(init_despesas_query)

        init_orgaos_query = """
            WITH 'https://dadosabertos.camara.leg.br/api/v2/deputados/{id}/orgaos?dataInicio=2019-01-01&itens=100000&ordem=ASC&ordenarPor=dataInicio'""".format(id=id) + """ AS url
            CALL apoc.load.json(url) YIELD value
            UNWIND value.dados as orgaos
            """ + "MATCH (dep:Deputado {id:" +str(id) +"})" + """
            FOREACH(orgao in orgaos |
                MERGE (o:Orgao {idOrgao: TOINT(orgao.idOrgao)})
                    ON CREATE SET o.uriOrgao = orgao.uriOrgao, o.siglaOrgao = orgao.siglaOrgao, o.nomeOrgao = orgao.nomeOrgao
                
                CREATE (dep)-[:PARTICIPA {titulo: orgao.titulo, dataInicio: DATE(left(orgao.dataInicio,10)), dataFim: DATE(left(orgao.dataFim,10))}]->(o)
            )
        """
        graph.run(init_orgaos_query)
    
    get_partyIds_query = """
        WITH 'https://dadosabertos.camara.leg.br/api/v2/partidos?itens=10000&ordem=ASC&ordenarPor=sigla' AS url
        CALL apoc.load.json(url) YIELD value
        UNWIND value.dados as dados
        RETURN dados.id
    """
    partyIds = [r['dados.id'] for r in graph.run(get_partyIds_query)]

    for id in partyIds:
        init_party_query = """
            WITH 'https://dadosabertos.camara.leg.br/api/v2/partidos/{id}'""".format(id=id) + """ AS url
            CALL apoc.load.json(url) YIELD value
            UNWIND value.dados as dados

            WITH dados
            MATCH (p: Partido {sigla: dados.sigla})
            MATCH (d:Deputado {nome: dados.status.lider.nome})
            MERGE (d)-[:LIDER]-(p)
            SET p.id = TOINT(dados.id), p.nome = dados.nome, p.situacao = dados.status.situacao,
            p.totalMembros = TOINT(dados.status.totalMembros), p.urlLogo = dados.urlLogo
        """
        graph.run(init_party_query)


def get_deputados():
    query = """
        MATCH(dep:Deputado)
        RETURN dep.nomeCivil
    """

    deputados = []
    for record in graph.run(query):
        deputados.append(record["dep.nomeCivil"])
    
    return deputados
