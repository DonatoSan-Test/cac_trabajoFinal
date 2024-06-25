from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
import time

class Usuarios:
    def __init__(self, host, user, password, database):
        self.conexion= mysql.connector.connect(host=host,user=user,password=password,database=database)
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
      

# ------------------------------------------------------
# programa principal
# ------------------------------------------------------
##Conexion a la Base de Datos
usuarios= Usuarios("localhost","root","","mybbdd")

##Agregar un contacto
#usuario.agregar_contacto("codoAcodo-2024","codoAcodo-2024@gmail.com","1147044000","Consulta","Este es el primer mensaje para codo a codo gaming",1)

##Mostrar un contacto
#usuario.mostrar_contacto(2)

##Modificar Contacto
#usuario.modificar_contacto(2,"Fullstack-25","fullstack-25@gmail.com","1145500555","Consulta","Soy fullstack listo para programar",0)

##Listar todos los contactos
#usuario.listar_contactos()
#######################################
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('home.html', title='Prueba Flask', 
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
    new_gamertag = request.form.get['gamertag']
    new_email = request.form.get['email']
    new_telefono = request.form.get['telefono']    
    new_motivo = request.form.get['motivo']
    new_mensaje = request.form.get['mensaje']    
    new_suscripcion = request.form.get['suscripcion']

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






