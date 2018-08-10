'''
Created on 6 ago. 2018

@author: formijor
'''

#https://medium.com/@betz.mark/cross-thread-event-dispatching-in-python-fc956446ad16

import threading
import queue

class hilo_pool():
    def __init__(self, conexion_archivo):
        self.conexion_hilo(conexion_archivo)        
        
    def conexion_hilo(self, conexion_archivo):
        pass    
    
    def recibir_mensajes_cliente(self):
        pass
    
    def enviar_mensaje_cliente(self):
        pass
    
    def recibir_mensajes_pool(self):
        pass
    
    def enviar_mensaje_pool(self):
        pass
    

class pool_hilo_principal():
    def __init__(self):
        self.obtener_cantidad_threads()
        print ("Hilo Principal ejecutandose")
            
    def escuchar_hilos(self):
        while threading.active_count() > thread_count:
            event = msg_queue.get()
            event()
    
    def crear_cola(self):
        cola_espera = queue.Queue()
        
    def obtener_cantidad_threads(self):
        self.thread_cantidad = threading.active_count()
        

if __name__ == "__main__":
    thread = threading.Thread(target = pool_hilo_principal)#, args = (10, ))
    thread.start()
    thread.join()
    print ("thread finished...exiting")