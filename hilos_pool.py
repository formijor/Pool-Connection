'''
Created on 6 ago. 2018

@author: formijor
'''

#https://medium.com/@betz.mark/cross-thread-event-dispatching-in-python-fc956446ad16

import threading
import queue
import time

class hilo_pool():
    def __init__(self, conexion_archivo, cola_espera_in, cola_espera_out):
        print (threading.currentThread().getName(), 'Iniciando')
        self.conexion_hilo(conexion_archivo)     
        self.cola_espera_in = cola_espera_in
        self.cola_espera_out = cola_espera_out
        time.sleep(2) 
        self.enviar_mensaje_pool('\nAAAAAH\n---------------------\n')
        self.recibir_mensajes_pool()
        
    def conexion_hilo(self, conexion_archivo):
        pass    
    
    def recibir_mensajes_cliente(self):
        pass
    
    def enviar_mensaje_cliente(self):
        pass
    
    def recibir_mensajes_pool(self):
        while 1:
            mensaje = self.cola_espera_in.get()
            print (threading.currentThread().getName() + mensaje)  
        
          
    def enviar_mensaje_pool(self, mensaje):
        self.cola_espera_out.put(mensaje)
    
    def imprimir_mensaje(self, mensaje):
        print(mensaje)



class pool_hilo_principal():
    def __init__(self):
        print ("Hilo Principal ejecutandose\n")
        self.obtener_cantidad_threads()
        self.crear_cola()
        self.lista_hilos = {}
        self.crear_hilos()
        self.recibir_mensajes_hilos()               
        self.finalizar_pool()        
        
    def crear_hilos(self):        
        cliente = ['Jorge', 'Carolina', 'doña']
        for x in range(3):
            nombre = cliente.pop()        
            self.hilo = threading.Thread(target = hilo_pool, args = ("HOLA", self.cola_espera_in, self.cola_espera_out), name = nombre)
            self.lista_hilos[nombre] = (self.hilo, self.cola_espera_in, self.cola_espera_out)
            self.hilo.start()        
            
    def recibir_mensajes_hilos(self):
        '''while threading.active_count() > self.thread_cantidad_inicial:        
        event = self.cola_espera_out.get()
        print (event)'''
        time.sleep(6)
        self.enviar_mensajes_hilos() 
    
    def enviar_mensajes_hilos(self):
        print (self.lista_hilos)
        hilo = self.lista_hilos['Carolina']
        hilo[1].put('\nAy Caramba\n')
       
    def crear_cola(self):
        self.cola_espera_in = queue.Queue()
        self.cola_espera_out = queue.Queue()        
        
    def obtener_cantidad_threads(self):
        self.thread_cantidad_inicial = threading.active_count()
        print (self.thread_cantidad_inicial)
    
    def hilo_esta_activo(self, hilo):
        return hilo.is_alive()        
    
    def finalizar_pool(self):
        for hilo in self.lista_hilos.values():
            print (hilo)
            hilo[0].join()
        print ("pool finalizada... Desconectando")

if __name__ == "__main__":
    pool_hilo_principal()
    