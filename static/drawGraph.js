function draw(cypher){
    var config = {
	container_id: "vis",
        server_url: "bolt://ec2-34-237-60-91.compute-1.amazonaws.com:7687",
        server_user: "neo4j",
        server_password: "ihc",
        labels: {
            "Partido": {
                size: "totalMembros",
                caption: "sigla"
            },
            "Deputado": {
                caption: "nome"
            },
            "Municipio": {
                caption: "nome"
            },
            "UnidadeFederativa": {
                caption: "sigla"
            },
            "Despesa": {
                caption: "nomeFornecedor"
            },
            "Orgao": {
                caption: "siglaOrgao"
            },
            "Demonstracao": {
                size: "n",
                caption: "nome"
            },
            "Demonstracao2": {
                size: "percentual",
                caption: "nome"
            },
            "PartidoExpense": {
                size: "valor",
                caption: "sigla"
            }
        },
        relationships: {
            "FILIADO": {
                caption: false
            },
            "GASTOU": {
                caption: "data"
            }
        },
        initial_cypher: cypher,
        arrows: true,
    }
    var viz = new NeoVis.default(config)
    viz.render()
}
