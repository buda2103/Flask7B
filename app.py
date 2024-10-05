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
def notificarActualizacizarTelefonoArchivo():
pusher_client = pusher.Pusher(
    app_id="1867163",
    key="2358693f2b619b363f59",
    secret="880f60b50e86e4555c43",
    cluster="us2",
    ssl=True
)
    pusher_client.trigger("CanalPago_curso", "pago-curso", args)

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
    cursor.execute("""
    "SELECT  Id_Curso_Pago  Telefono, Archivo FROM tst0_cursos_pagos 
    ORDER BY Id_Curso_Pago DESC
    LIMIT 10 OFFSET 0
    """)
    
    registros = cursor.fetchall()

    con.close()

    return make_response(jsonify(registros))
# Ruta para registrar un nuevo pago y activar el evento Pusher
@app.route("/registrar", methods=["POST"])
def registrar():
    if not con.is_connected():
        con.reconnect()
                                 
    id       = request.form["id"]
    Telefono = request.form["Telefono"]
    Archivo  = request.form["Archivo"]
    
    cursor = con.cursor()

    if id:
        sql = """
        UPDATE tst0_cursos_pagos SET
        Telefono = %s,
        Archivo     = %s
        WHERE Id_Curso_Pago = %s
        """
        val = (Telefono, Archivo, id)
    else:
        sql = """
        INSERT INTO tst0_cursos_pagos (Telefono, Archivo)
                        VALUES (%s,          %s)
        """
        val =                  (Telefono, Archivo)
    
    cursor.execute(sql, val)
    con.commit()
    cursor.close()

    notificarActualizacizarTelefonoArchivo()    
    return make_response(jsonify({}))
    
# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
