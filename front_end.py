from flask import Flask, render_template, request
from back_end import CamaraDosDeputados

name = "APPLICATION" #"__main__"

app = Flask(name)

camaraDosDeputados = CamaraDosDeputados()
#camaraDosDeputados.init_db()

@app.route("/", methods=('GET', 'POST'))
def home():
    return render_template("home.html", cypher=camaraDosDeputados.get_all_query())

@app.route("/deputados/", methods=('GET', 'POST'))
def deputados():
    deputados = camaraDosDeputados.get_deputados()
    return render_template("deputados.html", deputados=deputados, cypher=camaraDosDeputados.get_deputados_query())

@app.route("/deputados/<deputado>")
def ficha_deputado(deputado):
    return deputado

@app.route("/partidos/")
def partidos():
    partidos = camaraDosDeputados.get_partidos()
    return render_template("partidos.html", partidos=partidos, cypher=camaraDosDeputados.get_partidos_query())

@app.route("/partidos/<partido>")
def ficha_partido(partido):
    return partido;

@app.route("/orgaos/")
def orgaos():
    orgaos = camaraDosDeputados.get_orgaos()
    return render_template("orgaos.html", orgaos=orgaos, cypher=camaraDosDeputados.get_orgaos_query())

@app.route("/orgaos/<orgao>")
def ficha_orgao(orgao):
    return orgao

if name == "__main__":
    app.run(debug=True)
else:
    app.run()

