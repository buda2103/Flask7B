from flask import Flask

from flask import render_template
from flask import request

import pusher

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")
 @app.route("/Pago_Curso")
def index():
    return render_template("Pago_Curso.html")

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    matricula      = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    return f"Matrícula {matricula} Nombre y Apellido {nombreapellido}"

def evento ():
 pusher_client = pusher.Pusher(
app_id = "1867163"
key = "2358693f2b619b363f59"
secret = "880f60b50e86e4555c43"
cluster = "us2"
)
pusher_client.trigger("my-channel", "my-event", {})
