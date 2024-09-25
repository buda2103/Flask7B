from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector
import datetime
import pytz

# Configuración de la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configurar Pusher
pusher_client = pusher.Pusher(
    app_id="1867163",
    key="2358693f2b619b363f59",
    secret="880f60b50e86e4555c43",
    cluster="us2",
    ssl=True
)

# Página principal
@app.route("/")
def index():
    return render_template("Pago-Curso.html")

# Ruta para buscar pagos en la base de datos
@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_cursos_pagos ORDER BY Id_Curso_Pago DESC")
    registros = cursor.fetchall()

    con.close()

    return registros

# Ruta para registrar un nuevo pago y activar el evento Pusher
@app.route("/registrar", methods=["GET"])
def registrar():
    args = request.args

    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    # Insertar el registro en la base de datos
    sql = "INSERT INTO tst0_cursos_pagos (Telefono, Archivo, Fecha) VALUES (%s, %s, %s)"
    val = (
        args["Telefono"], 
        "Hola", 
        datetime.datetime.now(pytz.timezone("America/Matamoros"))
    )
    cursor.execute(sql, val)
    
    # Confirmar los cambios
    con.commit()
    cursor.close()

    # Activar el evento en Pusher
    pusher_client.trigger("CanalPago_curso", "pago-curso", args)
    
    return "Evento registrado con éxito"

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
