from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

# Configuración de conexión SQL Server
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=DESKTOP-UAR8JQO\\SQLEXPRESS;'
                      'DATABASE=CatequisisModelo;'
                      'UID=Catequesis;PWD=catequesisudla')
cursor = conn.cursor()

@app.route('/')
def index():
    # Cargar niveles y parroquias desde la base de datos
    cursor.execute("SELECT Id_Nivel, Parroquia_Bautismo, Horario FROM NivelCatequesis")
    niveles = cursor.fetchall()

    cursor.execute("SELECT Id_Parroquia, Nombre_Parroquia FROM Parroquia")
    parroquias = cursor.fetchall()

    return render_template('index.html', niveles=niveles, parroquias=parroquias)

@app.route('/registrar', methods=['POST'])
def registrar():
    id_nivel = request.form['id_nivel']
    id_parroquia = request.form['id_parroquia']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    domicilio = request.form['domicilio']
    cedula = request.form['cedula']
    horario = request.form['horario']

    nombre_completo = f"{nombre} {apellido}"

    # Obtener el nombre de la parroquia a partir del ID
    cursor.execute("SELECT Nombre_Parroquia FROM Parroquia WHERE Id_Parroquia = ?", (id_parroquia,))
    parroquia_row = cursor.fetchone()
    parroquia = parroquia_row.Nombre_Parroquia if parroquia_row else "Desconocida"

    # Insertar en la tabla Catequizado
    query = "INSERT INTO Catequizado (Nombre, Parroquia_Bautismo, Horario, Id_Nivel) VALUES (?, ?, ?, ?)"
    cursor.execute(query, (nombre_completo, parroquia, horario, id_nivel))
    conn.commit()
    return redirect('/')

@app.route('/ver')
def ver():
    cursor.execute("SELECT Id_Catequizado, Nombre, Parroquia_Bautismo, Horario, Id_Nivel FROM Catequizado")
    catequizados = cursor.fetchall()
    return render_template('ver.html', catequizados=catequizados)

if __name__ == '__main__':
    app.run(debug=True)
