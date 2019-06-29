function draw(cypher){
    var config = {
        container_id: "vis",
        server_url: "bolt://localhost:7687",
        server_user: "gui",
        server_password: "abc",
        labels: {
            "Partido": {
                size: "totalMembros",
                caption: "sigla"
            }
        },
        relationships: {
            "FILIADO": {
                caption: false
            }
        },
        initial_cypher: cypher
    }
    var viz = new NeoVis.default(config)
    viz.render()
}
