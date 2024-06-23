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

    def modificar_contacto(self,id_contacto,new_gamertag,new_email,new_telefono,new_motivo,new_mensaje,new_suscripcion): #probado exitosamente
        sql= "UPDATE contactos SET gamertag=%s,email=%s,telefono=%s,motivo=%s,mensaje=%s,suscripcion=%s WHERE id_contacto=%s"
        valores= (new_gamertag,new_email,new_telefono,new_motivo,new_mensaje,new_suscripcion,id_contacto)
        self.cursor.execute(sql, valores)
        self.conexion.commit()
        return self.cursor.rowcount > 0

    def mostrar_contacto(self,id_contacto): #probado exitosamente
        self.cursor.execute(f"SELECT * FROM contactos WHERE id_contacto={id_contacto}")
        contacto= self.cursor.fetchone()
        return contacto

    def listar_contactos(self): #probado exitosamente
        self.cursor.execute("SELECT * FROM contactos")
        contactos= self.cursor.fetchall()        
        return contactos
    
    def eliminar_contacto(self,id_contacto):
        self.cursor.execute(f"DELETE FROM contactos WHERE id_contacto={id_contacto}")
        self.conexion.commit()
        return self.cursor.rowcount() > 0

#programa principal
##Conexion a la Base de Datos
usuarios= Usuarios("localhost","root","","mybbdd")

##Agregar un contacto
#usuario.agregar_contacto("Fullstack-24","fullstack-24@gmail.com","1145500849","Consulta","Soy fullstack listo para programar",0)

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


if __name__ == "__main__":
    app.run(debug=True)






