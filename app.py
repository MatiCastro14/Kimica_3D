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
   

    #----------------------------------------------------------------
    def modificar_consulta(self, id, nombre, correo, telefono, imagen, motivo, preferencia, comentario):
        sql = "UPDATE consultas SET nombre = %s, correo_electronico = %s, telefono = %s, imagen_url = %s, motivo = %s, preferencia = %s, comentario = %s WHERE id = %s"
        valores = (nombre, correo, telefono, imagen, motivo, preferencia, comentario, id)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0


    #----------------------------------------------------------------

    def consultar_contacto(self, id):
        # Consultamos un consulta a partir de su código
        self.cursor.execute(f"SELECT * FROM consultas WHERE id = {id}")
        return self.cursor.fetchone()
#------------------------------------------------------------------------------
    def mostrar_consulta(self, id):
        # Mostramos los datos de un consulta a partir de su código
        consulta = self.consultar_contacto(id)
        if consulta:
            print("-" * 40)
            print(f"id.....: {consulta['id']}")
            print(f"nombre: {consulta['nombre']}")
            print(f"correo_electronico...: {consulta['correo_electronico']}")
            print(f"telefono.....: {consulta['telefono']}")
            print(f"preferencia.....: {consulta['preferencia']}")
            print(f"comentario..: {consulta['comentario']}")
            print(f"motivo..: {consulta['motivo']}")
            print(f"imagen_url..: {consulta['imagen_url']}")
            print("-" * 40)
        else:
            print("consulta no encontrado.")


#----------------------------------------------------------------
    def listar_consultas(self):
        self.cursor.execute("SELECT * FROM consultas")
        consulta = self.cursor.fetchall()
        return consulta
 #----------------------------------------------------------------
    def eliminar_consulta(self, id):
        # Eliminamos un consulta de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM consultas WHERE id = {id}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------
# Crear una instancia de la clase Catalogo
#contacto = Contacto(host='localhost', user='root', password='root', database='miapp')
contacto = Contacto(host='mcastro.mysql.pythonanywhere-services.com', user='mcastro', password='J5r2t7f8', database='mcastro$miapp')


# Carpeta para guardar las imagenes.
#RUTA_DESTINO = './static/imagenes/'

#Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
RUTA_DESTINO = '/home/mcastro/mysite/static/imagenes'


#--------------------------------------------------------------------
# Listar todos los consultas
#--------------------------------------------------------------------
#La ruta Flask /consultas con el método HTTP GET está diseñada para proporcionar los detalles de todos los consultas almacenados en la base de datos.
#El método devuelve una lista con todos los consultas en formato JSON.

@app.route("/consultas", methods=["GET"])
def listar_consultas():
    consulta = contacto.listar_consultas()
    return jsonify(consulta)





#--------------------------------------------------------------------
# Listar por su id
#--------------------------------------------------------------------
@app.route("/consultas/<int:id>", methods=["GET"])
def mostrar_contacto(id):
    consulta = contacto.consultar_contacto(id)
    if consulta:
        return jsonify(consulta), 201
    else:
        return "Consulta no encontrado", 404



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
# Modificar un consulta según su código
#--------------------------------------------------------------------
@app.route("/consultas/<int:id>", methods=["PUT"])
def modificar_consulta(id):

    # Recuperar los nuevos datos del formulario
    nombre = request.form.get("nombre")
    correo = request.form.get("correo")
    telefono = request.form.get("telefono")
    motivo = request.form.get("motivo")
    preferencia = request.form.get("preferencia")
    comentario = request.form.get("comentario")

    # Verificar si se proporciona una nueva imagen
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        # Procesar la imagen
        nombre_imagen = secure_filename(imagen.filename)
        nombre_base, extension = os.path.splitext(nombre_imagen)
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))
    else:
        # Si no se proporciona una nueva imagen, mantener la imagen existente
        consulta = contacto.consultar_contacto(id)
        if consulta:
            nombre_imagen = consulta["imagen_url"]

    # Llamar al método modificar_consulta pasando el id y los nuevos datos
    if contacto.modificar_consulta(id, nombre, correo, telefono, nombre_imagen, motivo, preferencia, comentario):
        return jsonify({"mensaje": "Consulta modificada correctamente."}), 200
    else:
        return jsonify({"mensaje": "Error al modificar la consulta."}), 500

@app.route("/consultas/<int:id>", methods=["GET"])
def mostrar_consulta(id):
    consulta = contacto.consultar_contacto(id)
    if consulta:
        return jsonify(consulta), 201
    else:
        return "Consulta no encontrada.", 404


#--------------------------------------------------------------------
# Eliminar un consulta según su código
#--------------------------------------------------------------------
@app.route("/consultas/<int:id>", methods=["DELETE"])

def eliminar_consulta(id):

    consulta = contacto.consultar_contacto(id)
    if consulta: # Si existe, verifica si hay una imagen asociada en el servidor.
        imagen_vieja = consulta["imagen_url"]
        # Armo la ruta a la imagen
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

       
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

      
        if contacto.eliminar_consulta(id):
        
        
            return jsonify({"mensaje": "consulta eliminado"}), 200
        else:
            
            return jsonify({"mensaje": "Error al eliminar el consulta"}), 500
    else:
        
        return jsonify({"mensaje": "consulta no encontrado"}), 404


    #--------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)