from flask import Flask, render_template, request
import pusher

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/Registrar")
def alumnos():
    return render_template("Pago_Curso.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    matricula = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    return f"Matrícula {matricula}, Nombre y Apellido {nombreapellido}"

def evento():
    pusher_client = pusher.Pusher(
        app_id="1867163",
        key="2358693f2b619b363f59",
        secret="880f60b50e86e4555c43",
        cluster="us2",
        ssl=True  # Add this to use SSL if needed
    )
    pusher_client.trigger("my-channel", "my-event", {})
