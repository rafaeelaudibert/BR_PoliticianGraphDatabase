from py2neo import Graph, Node, Relationship


class CamaraDosDeputados:

    def __init__(self):
        # 1: username 2: password 3: port
        #                          |1 | 2 |          | 3 |
        self.graph = Graph("http://gui:abc@127.0.0.1:7474/db/data")

    def init_db(self):
        self.delete_all()
        self.create_constraints()

        self.depIds = self.get_dep_ids()
        self.partyIds = self.get_party_ids()

        self.init_deputados()
        self.init_despesas()
        self.init_orgaos()
        self.init_partidos()

    def delete_all(self):
        self.graph.run("MATCH(n) DETACH DELETE n")

    def create_constraints(self):
        self.graph.run("CREATE CONSTRAINT ON (d:Deputado) ASSERT d.nome is UNIQUE;")
        self.graph.run("CREATE CONSTRAINT ON (d:Deputado) ASSERT d.id is UNIQUE;")
        self.graph.run("CREATE CONSTRAINT ON (p:Partido) ASSERT p.sigla is UNIQUE;")
        self.graph.run("CREATE CONSTRAINT ON (m:Municipio) ASSERT m.nome is UNIQUE;")
        self.graph.run("CREATE CONSTRAINT ON (uf:UnidadeFederativa) ASSERT uf.sigla is UNIQUE;")
        self.graph.run("CREATE CONSTRAINT ON (o:Orgao) ASSERT o.idOrgao is UNIQUE;")

    def get_dep_ids(self):
        get_depIds_query = """
            WITH 'https://dadosabertos.camara.leg.br/api/v2/deputados?ordem=ASC&ordenarPor=nome' AS url
            CALL apoc.load.json(url) YIELD value
            UNWIND value.dados as dados
            RETURN dados.id
        """
        depIds = [r['dados.id'] for r in self.graph.run(get_depIds_query)]
        return depIds
    
    def get_party_ids(self):
        get_partyIds_query = """
            WITH 'https://dadosabertos.camara.leg.br/api/v2/partidos?itens=10000&ordem=ASC&ordenarPor=sigla' AS url
            CALL apoc.load.json(url) YIELD value
            UNWIND value.dados as dados
            RETURN dados.id
        """
        partyIds = [r['dados.id'] for r in self.graph.run(get_partyIds_query)]
        return partyIds
    
    def init_deputados(self):
        for id in self.depIds:
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
                    MERGE(m:Municipio {nome: dados.municipioNascimento})
                    MERGE(uf: UnidadeFederativa {sigla: dados.ufNascimento})
                    MERGE (d)-[:ORIGEM]->(m)
                    MERGE (m)-[:SITUADO]-(uf)
                )		
            """
            self.graph.run(init_deputado_query)
    
    def init_despesas(self):
        for id in self.depIds:
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
            self.graph.run(init_despesas_query)

    def init_orgaos(self):
        for id in self.depIds:
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
            self.graph.run(init_orgaos_query)

    def init_partidos(self):
        for id in self.partyIds:
            init_party_query = """
                WITH 'https://dadosabertos.camara.leg.br/api/v2/partidos/{id}'""".format(id=id) + """ AS url
                CALL apoc.load.json(url) YIELD value
                UNWIND value.dados as dados

                WITH dados
                MATCH (p:Partido {sigla: dados.sigla})
                MATCH (d:Deputado {nome: dados.status.lider.nome})
                MERGE (d)-[:LIDER]-(p)
                SET p.id = TOINT(dados.id), p.nome = dados.nome, p.situacao = dados.status.situacao,
                p.totalMembros = TOINT(dados.status.totalMembros), p.urlLogo = dados.urlLogo
            """
            self.graph.run(init_party_query)

    def get_all_query(self):
        return "\"MATCH a=(:Deputado)-[]-(:Partido) RETURN a\""

    def get_deputados_query(self):
        return "\"MATCH (d:Deputado) RETURN d\""

    def get_partidos_query(self):
        return "\"MATCH (p:Partido) RETURN p\""

    def get_orgaos_query(self):
        return "\"MATCH (o:Orgao) RETURN o\""

    def get_deputados(self):
        query = """
            MATCH(dep:Deputado)
            RETURN dep.nome
            ORDER BY dep.nome
        """
        deputados = []
        for record in self.graph.run(query):
            deputados.append(record["dep.nome"])
        return deputados

    def get_partidos(self):
        query = """
            MATCH(p:Partido)
            RETURN p.sigla
            ORDER BY p.totalMembros DESC
        """
        partidos = []
        for record in self.graph.run(query):
            partidos.append(record["p.sigla"])
        return partidos

    def get_orgaos(self):
        query = """
            MATCH(o:Orgao)
            RETURN o.siglaOrgao
            ORDER BY o.siglaOrgao
        """
        orgaos = []
        for record in self.graph.run(query):
            orgaos.append(record["o.siglaOrgao"])
        return orgaos


    def get_deputado_info(self, deputado_name):
        query = """
            MATCH (d:Deputado)
            WHERE d.nome =
        """
        query += '\"' + deputado_name + '\"'
        query += """
            RETURN d.nascimento, d.nomeCivil, d.urlFoto, d.cpf, d.escolaridade, d.sexo, d.nome, d.idLegislatura, d.id
        """
        for record in self.graph.run(query):
            return record


    def get_deputado_gasto(self, deputado_name):
        query = """
            MATCH (d:Deputado)-[:GASTOU]-(des:Despesa)
            WHERE d.nome =
        """
        query += '\"' + deputado_name + '\"'
        query += """
            RETURN round(100*SUM(des.valorDocumento))/100 AS gasto
        """
        for record in self.graph.run(query):
            return record
    

    def get_deputado_relations_query(self, deputado_name):
        query = "\"MATCH a=(d:Deputado)-[]-() WHERE d.nome = '" + deputado_name + "' RETURN a\""
        return query


    def get_partido_info(self, partido_name):
        query = """
            MATCH (p:Partido)
            WHERE p.sigla =
        """
        query += '\"' + partido_name + '\"'
        query += """
            RETURN p.totalMembros, p.sigla, p.situacao, p.nome, p.id, p.urlLogo
        """
        for record in self.graph.run(query):
            return record

    def get_partido_deputado(self, partido_name):
        query = """
            MATCH (d:Deputado)-[:FILIADO]-(p:Partido)
            WHERE p.sigla =
        """
        query += '\"' + partido_name + '\"'
        query += """
            RETURN d.nome
        """
        deputados = []
        for record in self.graph.run(query):
            deputados.append(record["d.nome"])
        return deputados


    def get_orgao_info(self, orgao_name):
        query = """
            MATCH (o:Orgao)
            WHERE o.siglaOrgao =
        """
        query += '\"' + orgao_name + '\"'
        query += """
            RETURN o.nomeOrgao, o.siglaOrgao, o.idOrgao
        """
        for record in self.graph.run(query):
            return record
