from flask import Flask, render_template, request
from example_be import CamaraDosDeputados

name = "APPLICATION" #"__main__"

app = Flask(name)

camaraDosDeputados = CamaraDosDeputados()
camaraDosDeputados.init_db()

@app.route("/", methods=('GET', 'POST'))
def home():
    return render_template("home.html")

@app.route("/candidatos", methods=('GET', 'POST'))
def candidatos():
    candidaturas = camaraDosDeputados.get_deputados()
    return render_template("candidato.html", candidaturas=candidaturas)

@app.route("/candidatos/<candidatura>")
def candidatura(candidatura):
    return candidatura

@app.route("/mandatos", methods=('GET', 'POST'))
def mandatos():
    return render_template("mandato.html") 

@app.route("/partidos", methods=('GET', 'POST'))
def partidos():
    return render_template("partido.html")

if name == "__main__":
    app.run(debug=True)
else:
    app.run()

