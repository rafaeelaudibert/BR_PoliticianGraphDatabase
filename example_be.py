from py2neo import Graph, Node, Relationship

#                     |1 | 2 |          | 3 |
graph = Graph("http://gui:abc@127.0.0.1:7474/db/data")
# 1: username
# 2: password
# 3: port

def initialize():
    jeff = Node("User", Name="Jeff", Age="20")
    ahmed = Node("User", Name="Ahmed", Age="40")
    john = Node("User", Name="John", Age="9")
    francis = Node("User", Name="Francis", Age="20")
    bowl = Node("Event", Name="Bowling Meetup", Day="02/01/1999", Location="Dairy County Bowling Alley")

    delete_query = """
        MATCH(n) DETACH DELETE n
    """

    graph.run(delete_query)
    
    init_deputados_query = """
        WITH 'https://dadosabertos.camara.leg.br/api/v2/deputados?ordem=ASC&ordenarPor=nome' AS url
        CALL apoc.load.json(url) YIELD value
        UNWIND value.dados as dados
        CREATE(d:Deputado {Nome : dados.nome})
    """
    graph.run(init_deputados_query)

"""
    graph.create(jeff)
    graph.create(Relationship(ahmed, "WENT", bowl))
    graph.create(Relationship(john, "WENT", bowl))
    graph.create(Relationship(francis, "WENT", bowl))
    graph.create(Relationship(john, "FATHER", francis))
"""
def get_deputados():
    query = """
        MATCH(dep:Deputado)
        RETURN dep.Nome
    """

    deputados = []
    for record in graph.run(query):
        deputados.append(record["dep.Nome"])
    
    return deputados
