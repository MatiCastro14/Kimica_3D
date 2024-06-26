#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify, render_template
from flask import request

# Instalar con pip install flask-cors
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#--------------------------------------------------------------------



app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas

#--------------------------------------------------------------------
class Contacto:
    #----------------------------------------------------------------
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS consultas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            correo_electronico VARCHAR(255) NOT NULL,
            telefono INT NOT NULL,
            preferencia VARCHAR(255),
            comentario VARCHAR(255),
            motivo VARCHAR(25) NOT NULL,
            imagen_url VARCHAR(255))''')
        self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
        

        
    #----------------------------------------------------------------
    def agregar_consulta(self,nombre, correo, telefono,imagen, motivo,preferencia,comentario):
               
        sql = "INSERT INTO consultas (nombre, correo_electronico, telefono, imagen_url, motivo,preferencia,comentario) VALUES (%s, %s, %s, %s, %s,%s,%s)"
        valores = (nombre, correo, telefono, imagen, motivo,preferencia,comentario)

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return self.cursor.lastrowid
    


#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------
# Crear una instancia de la clase Catalogo
contacto = Contacto(host='localhost', user='root', password='root', database='miapp')
#contacto = contacto(host='USUARIO.mysql.pythonanywhere-services.com', user='USUARIO', password='CLAVE', database='USUARIO$miapp')


# Carpeta para guardar las imagenes.
RUTA_DESTINO = './static/imagenes/'

#Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
#RUTA_DESTINO = '/home/USUARIO/mysite/static/imagenes'


#--------------------------------------------------------------------
# Listar todos los consultas
#--------------------------------------------------------------------
#La ruta Flask /consultas con el método HTTP GET está diseñada para proporcionar los detalles de todos los consultas almacenados en la base de datos.
#El método devuelve una lista con todos los consultas en formato JSON.
#@app.route("/contacto", methods=["GET"])
#def listar_consultas():
    #consultas = contacto.listar_consultas()
   # return jsonify(consultas)


    #--------------------------------------------------------------------
# Agregar un consulta
#--------------------------------------------------------------------
@app.route("/consultas", methods=["POST"])
#La ruta Flask `/consultas` con el método HTTP POST está diseñada para permitir la adición de un nuevo consulta a la base de datos.
#La función agregar_consulta se asocia con esta URL y es llamada cuando se hace una solicitud POST a /consultas.
def agregar_consulta():
    #Recojo los datos del form
    nombre = request.form['nombre']
    correo = request.form['correo']
    telefono = request.form['telefono']
    imagen = request.files['foto']
    motivo = request.form['motivo']
    preferencia= request.form ['preferencia']
    comentario= request.form['comentario']
    nombre_imagen=""

    
    # Genero el nombre de la imagen
    nombre_imagen = secure_filename(imagen.filename) #Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
    nombre_base, extension = os.path.splitext(nombre_imagen) #Separa el nombre del archivo de su extensión.
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" #Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.

    nuevo_id = contacto.agregar_consulta(nombre, correo, telefono, nombre_imagen, motivo,preferencia,comentario)
    if nuevo_id:    
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))

        #Si el consulta se agrega con éxito, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 201 (Creado).
        return jsonify({"mensaje": "consulta agregado correctamente.", "id": nuevo_id, "imagen": nombre_imagen}), 201
    else:
        #Si el consulta no se puede agregar, se devuelve una respuesta JSON con un mensaje de error y un código de estado HTTP 500 (Internal Server Error).
        return jsonify({"mensaje": "Error al agregar el consulta."}), 500
    


    #--------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)