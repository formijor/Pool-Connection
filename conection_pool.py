'''
Created on 7 ago. 2018

@author: JorInt
'''

import sqlite3
import random
import time


class PoolConexiones():
    def __init__(self, numero_maximo_conexiones):
        self.numero_conexiones = numero_maximo_conexiones
        self.pool_conexiones = {}
        self.conectar_pool('Data\pool_config.db')
        
    def conectar_pool(self, archivo):
        self.conexion_pool = sqlite3.connect(archivo)
        self.cursor_pool = self.conexion_pool.cursor()
        print ('Conexion Establecida')
        
    def obtener_conexiones_activas(self):
        sql = "SELECT * FROM vista_conexiones_activas"
        self.cursor_pool.execute(sql)
        datos = self.cursor_pool.fetchall()
                   
    def guardar_nueva_conexion(self, conexion):
        fecha = time.strftime("%x")
        hora = time.strftime("%H:%M:%S")
        sql = """BEGIN;
                    INSERT INTO conexiones (codigo, archivo, fecha_conexion, hora_conexion)
                    VALUES """ + str((conexion.codigo, conexion.archivo, fecha, hora)) + """;
                     INSERT INTO conexiones_activas (id_conexion_activa, codigo_activa)
                    VALUES ((SELECT MAX(id_conexion) FROM conexiones), """ + str(conexion.codigo) + "); COMMIT;"      
        self.cursor_pool.executescript(sql)
        self.conexion_pool.commit()
        
    def generar_codigo_identificacion_conexion(self):
        codigo = random.randint(100, 999)
        sql = " SELECT * FROM conexiones WHERE codigo = " + str(codigo) + " AND codigo = (SELECT codigo FROM vista_conexiones_activas) "
        sql += " LIMIT 1;"
        self.cursor_pool.execute(sql)
        dato_codigo = self.cursor_pool.fetchall()
        while codigo in self.pool_conexiones or codigo in dato_codigo:
            self.generar_codigo_identificacion_conexion(self)                
        return codigo
        
    def crear_conexion(self, archivo, cliente):
        mensaje = 'Establecer conexion'
        codigo_conexion = self.generar_codigo_identificacion_conexion()
        conectado = Conexion(codigo_conexion, cliente, archivo)
        self.pool_conexiones[codigo_conexion] = conectado
        self.guardar_nueva_conexion(conectado)
        return conectado
    
    def finalizar_conexion(self, conexion):
        self.pool_conexiones.pop(conexion.codigo)
        conexion.cerrar_conexion()
        return True
        
    def finalizar_conexion_cliente(self, conexion):
        fecha = time.strftime("%x")
        hora = time.strftime("%H:%M:%S")
        sql = "UPDATE conexiones SET fecha_desconexion = " + "'"+fecha+"'"
        sql += ", hora_desconexion = " + str('"'+hora+'"')
        sql += "WHERE codigo = " + str(conexion.codigo) + " AND (fecha_desconexion is Null OR fecha_desconexion = 0);"        
        self.cursor_pool.execute(sql)
        self.conexion_pool.commit()
        conexion_terminada = self.finalizar_conexion(conexion)
        return conexion_terminada        
   
    def imprimir_conexiones_activas(self, datos):
        print("CONEXIONES ACTIVAS \n------------------------------")
        columnas = ('id_conexiones_activas', 'codigo', 'archivo', 'fecha_conexion', 'hora_conexion')
        for D in datos:
            for cont in range(len(columnas)):
                print (columnas[cont] + ": " + str(D[cont]))
            print ("\n-------------------------------")
           
    def borrar_datos_tablas(self, bd):
        sql = "DELETE FROM " + bd
        self.cursor_pool.execute(sql)
        self.conexion_pool.commit()
    
    def cerrar_conexiones_activas(self):
        fecha = time.strftime("%x")
        hora = time.strftime("%H:%M:%S")
        sql = "UPDATE conexiones SET fecha_desconexion = " + fecha
        sql += " , hora_desconexion = " + str('"' + hora + '"')
        sql += " WHERE fecha_desconexion is Null or fecha_desconexion = 0"
        self.cursor_pool.execute(sql)
        self.conexion_pool.commit()
        self.pool_conexiones = {}        
    
    def test(self, sql):
        self.cursor_pool.execute(sql)
        datos = self.cursor_pool.fetchall()
        return datos
    

class Conexion():
    def __init__(self, codigo, cliente, archivo):
        self.codigo = codigo
        self.cliente = cliente
        self.archivo = archivo
        self.cola_mensajes = []
        self.iniciar_conexion()
    
    def iniciar_conexion(self):
        self.conexion = sqlite3.connect(self.archivo)
        self.cursor = self.conexion.cursor()
        return True
    
    def cerrar_conexion(self):
        self.cursor.close()
        self.conexion.close()
        print ('Conexion ' + str(self.codigo) + ' Terminada')       
        return True
    
    def obtener_datos_conexion(self):
        return {"Codigo": self.codigo, "Cliente": self.cliente, "Archivo": self.archivo}
      
        
        
#---------------------------TEST--------------------   


def test_conection_pool(borrar, terminar):  
    print('Conectando con el pool de conexiones..') 
    pool = PoolConexiones(5)
    
    print('\nBuscando conexiones activas...')
    print (str(pool.test("SELECT count(id_conexion_activa) FROM conexiones_Activas")[0][0]) + " conexiones activas")
    
    print("\nConectando usuario 1...")
    usuario1 = pool.crear_conexion('Data\guardias_data.db', 'Jorge')
    print ("Conexion Establecida")
    
    print ("\nDatos de conexion:\n--------------------")
    imprimir = usuario1.obtener_datos_conexion()
    for dato in imprimir.items():
        print(dato[0] + ": " + str(dato[1]))
    
    if terminar is True:    
        print ("\nTerminar Conexion usuario 1...")
        resultado = pool.finalizar_conexion_cliente(usuario1)
        if resultado is True:
            print ("Conexion usuario 1 terminada") 
        elif resultado is False:
            print ("ERROR al desconectar usuario 1") 
    
    if borrar is True:
        pool.borrar_datos_tablas('conexiones_activas')
        pool.borrar_datos_tablas('conexiones')
        pool.borrar_datos_tablas('log')
        print ("\nTodos los registros fueron borrados")
    elif borrar == 'Informar':
        print (pool.test("SELECT * FROM Log"))
        print (pool.test("SELECT * FROM conexiones"))

test_conection_pool(True, True)