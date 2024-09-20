from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector

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
    cursor.execute("SELECT * FROM tst0_cursos_pagos")
    registros = cursor.fetchall()
    cursor.close()
    return jsonify(registros)  # Retorna los registros en formato JSON

# Ruta para registrar un nuevo pago y activar el evento Pusher
@app.route("/registrar", methods=["GET"])
def registrar():
    data = {
        "Telefono": request.args.get("Telefono"),
        "Archivo": request.args.get("Archivo")
    }
    mycursor = mydb.cursor()

sql = "INSERT INTO tst0_cursos_pagos (Telefono, Archivo) VALUES (%s, %s)"
val = (args["Telefono"], args["Archivo"], datetime.datetime.now(pytz.timezone("America/Matamoros")))
mycursor.execute(sql, val)

 con.commit()
    # Activar el evento en Pusher
    pusher_client.trigger("CanalPago_curso", "pago-curso", data)
    return "Evento registrado con éxito"

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
