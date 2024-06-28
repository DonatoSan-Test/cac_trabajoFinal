from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
import time

class Usuarios:
    def __init__(self, host, user, password, database):
        self.conexion= mysql.connector.connect(host=host,user=user,password=password,database=database)

        self.cursor = self.conexion.cursor()
        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conexion.database = database
            else:
                raise err
        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS `contactos` (
                                `id_contacto` INT(3) NOT NULL AUTO_INCREMENT , 
                                `gamertag` VARCHAR(15) NOT NULL , 
                                `email` VARCHAR(35) NOT NULL , 
                                `telefono` VARCHAR(10) NULL , 
                                `motivo` VARCHAR(10) NOT NULL , 
                                `mensaje` VARCHAR(255) NOT NULL , 
                                `suscripcion` INT(1) NULL , 
                                PRIMARY KEY (`id_contacto`)) ENGINE = InnoDB;''')
        self.conexion.commit()
        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor= self.conexion.cursor(dictionary=True)

    def agregar_contacto(self,gamertag,email,telefono,motivo,mensaje,suscripcion): #probado exitosamente
        sql= "INSERT INTO contactos(gamertag, email, telefono, motivo, mensaje, suscripcion) VALUES (%s, %s, %s, %s, %s, %s)"
        valores= (gamertag, email, telefono, motivo, mensaje, suscripcion)
        self.cursor.execute(sql, valores)
        self.conexion.commit()
        return self.cursor.lastrowid

    def mostrar_contacto(self,id_contacto): #probado exitosamente
        self.cursor.execute(f"SELECT * FROM contactos WHERE id_contacto={id_contacto}")
        contacto= self.cursor.fetchone()
        return contacto

    def listar_contactos(self): #probado exitosamente
        self.cursor.execute("SELECT * FROM contactos")
        contactos= self.cursor.fetchall()        
        return contactos
    
    def modificar_contacto(self,id_contacto,new_gamertag,new_email,new_telefono,new_motivo,new_mensaje,new_suscripcion): #probado exitosamente
        sql= "UPDATE contactos SET gamertag=%s,email=%s,telefono=%s,motivo=%s,mensaje=%s,suscripcion=%s WHERE id_contacto=%s"
        valores= (new_gamertag,new_email,new_telefono,new_motivo,new_mensaje,new_suscripcion,id_contacto)
        self.cursor.execute(sql, valores)
        self.conexion.commit()
        return self.cursor.rowcount > 0

    def eliminar_contacto(self,id_contacto):
        self.cursor.execute(f"DELETE FROM contactos WHERE id_contacto={id_contacto}")
        self.conexion.commit()
        return self.cursor.rowcount > 0
      
#----------------------------------------------
# PROGRAMA PRINCIPAL
#----------------------------------------------
usuarios = Usuarios(host="127.0.0.1", user="root", password="", database="myprueba")
#usuarios = Usuarios(host="DonatoSan.mysql.pythonanywhere-services.com", user="DonatoSan", password="gamer2024", database="DonatoSan$mybbdd")
app = Flask(__name__)
CORS(app)

#ruta_destino= './static/imagenes/'
ruta_destino= '/home/DonatoSan/mysite/static/imagenes/'

@app.route('/')
def home():
    return render_template('prueba.html', title='Prueba Flask', 
    heading='Bienvenido a Codo a Codo Gaming', subtitulo="CRUD", items=['Create','Read','Update','Delete'])

# listar todos los contactos
@app.route("/contactos", methods=["GET"])
def listar_contactos():
    contactos= usuarios.listar_contactos()
    return jsonify(contactos)

@app.route("/contactos/<int:id_contacto>", methods=["GET"])
def mostrar_contacto(id_contacto):
    contacto= usuarios.mostrar_contacto(id_contacto)
    if contacto:
        return jsonify(contacto), 201
    else:
        return "Contacto no encontrado", 404
# Agregar/Insertar contacto
@app.route("/contactos", methods=["POST"])
def agregar_contacto():
    # Capturo los datos del form
    gamertag = request.form['gamertag']
    email = request.form['email']
    telefono = request.form['telefono']    
    motivo = request.form['motivo']
    mensaje = request.form['mensaje']    
    #suscripcion = request.form['suscripcion']
    if request.form.get("suscripcion"):
        suscripcion = 1
    else:
        suscripcion = 0

    nuevo_id_contacto= usuarios.agregar_contacto(gamertag,email,telefono,motivo,mensaje,suscripcion)

    if nuevo_id_contacto:
        return jsonify({"mensaje":"El nuevo contacto se agrego correctamente","codigo":nuevo_id_contacto}), 201
    else:
        return jsonify({"mensaje":"Error al agregar nuevo contacto"}), 400
    
@app.route("/contactos/<int:id_contacto>", methods=["PUT"])
def modificar_contacto(id_contacto):
    # Capturo los datos del form  
    # asi no funciona error en el metodo request.form.get[]
    """new_gamertag = request.form.get['gamertag']     
    new_email = request.form.get['email']
    new_telefono = request.form.get['telefono']    
    new_motivo = request.form.get['motivo']
    new_mensaje = request.form.get['mensaje']    
    new_suscripcion = request.form.get['suscripcion']"""
    # asi si funciona
    new_gamertag = request.form['gamertag']     
    new_email = request.form['email']
    new_telefono = request.form['telefono']    
    new_motivo = request.form['motivo']
    new_mensaje = request.form['mensaje']    
    new_suscripcion = request.form['suscripcion']
    
    contacto= usuarios.modificar_contacto(id_contacto,new_gamertag,new_email,new_telefono,new_motivo,new_mensaje,new_suscripcion)

    if contacto:
        return jsonify({"mensaje":"El contacto se modifico correctamente"}), 201
    else:
        return jsonify({"mesaje":"Error al modificar contacto. Contacto no encontrado"}), 403

@app.route("/contactos/<int:id_contacto>", methods=["DELETE"])
def eliminar_contacto(id_contacto):
    contacto= usuarios.mostrar_contacto(id_contacto)
    if contacto:        
        if usuarios.eliminar_contacto(id_contacto):
            return jsonify({"mensaje":"El contacto se eliminó correctamente"}), 201
        else:
            return jsonify({"mesaje":"Error al eliminar contacto."}), 403
    else:
        return jsonify({"mesaje":"Error, contacto no encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True)
