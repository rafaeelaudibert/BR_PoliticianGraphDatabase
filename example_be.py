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

    graph.create(Relationship(ahmed, "WENT", bowl))
    graph.create(Relationship(john, "WENT", bowl))
    graph.create(Relationship(francis, "WENT", bowl))
    graph.create(Relationship(john, "FATHER", francis))

def get_event_goers():
    query = """
        MATCH(usr:User)-[:WENT]->(ev:Event)
        RETURN usr.Name
    """

    goers = []
    for record in graph.run(query):
        goers.append(record["usr.Name"])
    
    return goers
