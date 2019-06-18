from flask import Flask, render_template, request
import example_be

name = "APPLICATION" #"__main__"

app = Flask(name)

#example_be.initialize()

@app.route("/", methods=('GET', 'POST'))
def home():
    return render_template("home.html")

@app.route("/candidatos", methods=('GET', 'POST'))
def candidatos():
    candidaturas = example_be.get_deputados()
    return render_template("candidato.html", candidaturas=candidaturas)

@app.route("/candidatos/<candidatura>")
def candidatura(candidatura):
    return candidatura;

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

