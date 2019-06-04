from flask import Flask, render_template, request
import example_be

name = "APPLICATION" #"__main__"

app = Flask(name)

example_be.initialize()

@app.route("/", methods=('GET', 'POST'))
def home():
    abc = example_be.get_event_goers()
    return render_template("home.html", abc=abc)

if name == "__main__":
    app.run(debug=True)
else:
    app.run()

