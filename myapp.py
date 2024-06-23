import mysql.connector

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
        return self.cursor.rowcount>0

    def mostrar_contacto(self,id_contacto): #probado exitosamente
        self.cursor.execute(f"SELECT * FROM contactos WHERE id_contacto={id_contacto}")
        contacto= self.cursor.fetchone()
        print(contacto)

    def listar_contactos(self): #probado exitosamente
        self.cursor.execute("SELECT * FROM contactos")
        contactos= self.cursor.fetchall()        
        for contacto in contactos:
            print(contacto)
    

#programa principal
##Conexion a la Base de Datos
usuario= Usuarios("localhost","root","","mybbdd")
##Agregar un contacto
#usuario.agregar_contacto("Fullstack-24","fullstack-24@gmail.com","114550084","Consulta","Soy fullstack listo para programar",0)

##Mostrar un contacto
#usuario.mostrar_contacto(2)

##Modificar Contacto
#usuario.modificar_contacto(1,"Fullstack-25","fullstack-25@gmail.com","114550055","Consulta","Soy fullstack listo para programar",0)

##Listar todos los contactos
usuario.listar_contactos()


# listar todos los contactos
"""@app.route("/contactos", methods=["GET"])
def listar_contactos():
    contactos= usuario.listar_contactos()
    return jsonify(contactos)

@app.route("/contactos/<int:>", methods=["GET"])"""
