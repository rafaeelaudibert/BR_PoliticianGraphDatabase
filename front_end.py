from flask import Flask, render_template, request
from back_end import CamaraDosDeputados

name = "APPLICATION"  # "__main__"

app = Flask(__name__)

camaraDosDeputados = CamaraDosDeputados()
camaraDosDeputados.init_db()


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html", cypher=camaraDosDeputados.get_all_query())


@app.route("/", methods=["POST"])
def home_post():
    newCypher = '"' + request.form.get("textbox") + " LIMIT 1000" + '"'
    return render_template("home.html", cypher=newCypher)


@app.route("/deputados/", methods=("GET", "POST"))
def deputados():
    deputados = camaraDosDeputados.get_deputados()
    return render_template("deputados.html", deputados=deputados, cypher=camaraDosDeputados.get_deputados_query())


@app.route("/deputados/<deputado>")
def ficha_deputado(deputado):
    dados = camaraDosDeputados.get_deputado_info(deputado)
    gastos = camaraDosDeputados.get_deputado_gasto(deputado)
    return render_template(
        "ficha_deputado.html",
        dados=dados,
        cypher=camaraDosDeputados.get_deputado_relations_query(deputado),
        gasto=gastos,
    )


@app.route("/partidos/")
def partidos():
    partidos = camaraDosDeputados.get_partidos()
    return render_template("partidos.html", partidos=partidos, cypher=camaraDosDeputados.get_partidos_query())


@app.route("/partidos/<partido>")
def ficha_partido(partido):
    dados = camaraDosDeputados.get_partido_info(partido)
    deputados = camaraDosDeputados.get_partido_deputado(partido)
    return render_template("ficha_partido.html", dados=dados, deputados=deputados)


@app.route("/orgaos/")
def orgaos():
    orgaos = camaraDosDeputados.get_orgaos()
    return render_template("orgaos.html", orgaos=orgaos, cypher=camaraDosDeputados.get_orgaos_query())


@app.route("/orgaos/<orgao>")
def ficha_orgao(orgao):
    dados = camaraDosDeputados.get_orgao_info(orgao)
    return render_template("ficha_orgao.html", dados=dados)


if name == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
else:
    app.run(host="0.0.0.0", port=5000)
