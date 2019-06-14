from flask import Flask, render_template, request
import example_be

name = "APPLICATION" #"__main__"

app = Flask(name)

example_be.initialize()

@app.route("/", methods=('GET', 'POST'))
def home():
    abc = example_be.get_event_goers()
    return render_template("home.html")

@app.route("/candidatos", methods=('GET', 'POST'))
def candidatos():
    candidaturas = ['2016', '2010']
    return render_template("candidato.html", candidaturas=candidaturas)

@app.route("/candidatura/<candidatura>")
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

