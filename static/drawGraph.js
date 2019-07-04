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
