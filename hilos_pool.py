'''
Created on 6 ago. 2018

@author: formijor
'''

#https://medium.com/@betz.mark/cross-thread-event-dispatching-in-python-fc956446ad16

#https://stackoverflow.com/questions/2933399/how-to-set-time-limit-on-raw-input
#http://l4wisdom.com/python/python_threads.php
#https://www.python-course.eu/input.php

import threading
import queue
import time

class hilo_pool():
    def __init__(self, conexion_archivo, cola_espera_in, cola_espera_out):
        print (threading.currentThread().getName(), 'Iniciando\n')
        self.conexion_hilo(conexion_archivo)     
        self.cola_espera_in = cola_espera_in
        self.cola_espera_out = cola_espera_out
        self.run()
    
    def run(self):
        mensaje = self.recibir_mensajes_pool()
        while mensaje != 'Desconectar':
            mensaje = threading.currentThread().getName() + ': CONECTADO'#input(threading.currentThread().getName() + ': Esperando mensaje...\n')
            self.enviar_mensaje_pool(mensaje)
            mensaje = self.recibir_mensajes_pool()
            self.imprimir_mensaje(mensaje)
        print ('FIN: ' + threading.currentThread().getName())         
        
        
    def conexion_hilo(self, conexion_archivo):
        pass    
    
    def recibir_mensajes_cliente(self):
        pass
    
    def enviar_mensaje_cliente(self):
        pass
    
    def recibir_mensajes_pool(self):
        mensaje = self.cola_espera_in.get()
        self.imprimir_mensaje('\nMensaje Recibido de pool para ' + threading.currentThread().getName() + ": " + mensaje)  
          
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
        self.run_pool()    
    
    def run_pool(self):
        cantidad_hilos_inicial = self.obtener_cantidad_threads()
        self.crear_hilos()
        time.sleep(2)
        for hilo in self.lista_hilos.values():
                hilo[1].put('Conectado\n')                
        contador = 0     
        while cantidad_hilos_inicial < self.obtener_cantidad_threads():
            contador_cliente = 0
            for cliente, hilo in self.lista_hilos.items():
                contador_cliente += 1
                print ('CANT_CLIENTES: ' + str(contador_cliente))
                mensaje = hilo[2].get()
                print('MENSSS:' + mensaje)
                if mensaje == 'Desconectar':
                    hilo[0].join()
                elif mensaje == None:
                    print('ENVIAR MENSAJE\n')
                    cliente = input('CLIENTE: ')
                    mensaje = input('MENSAJE: ')
                    self.enviar_mensajes_hilos(cliente, mensaje)
                else:
                    self.imprimir_mensaje('Mensaje Recibido de ' + cliente + ' para Pool: ' + mensaje)
            print(contador + 1)
        print('FIN POOL')      
        
    def crear_hilos(self):        
        cliente = ['Jorge', 'Carolina', 'Julio']
        for x in range(3):
            nombre = cliente.pop()    
            cola_espera = self.crear_cola()   
            self.hilo = threading.Thread(target = hilo_pool, args = ("HOLA", cola_espera[0], cola_espera[1]), name = nombre)
            self.lista_hilos[nombre] = (self.hilo, cola_espera[0], cola_espera[1])
            self.hilo.start()
            
    def recibir_mensajes_hilos(self):
        '''while threading.active_count() > self.thread_cantidad_inicial:        
        event = self.cola_espera_out.get()
        print (event)'''
        pass
        
    #def recibir_mensaje_hilos(self):
        
    
    def enviar_mensajes_hilos(self, cliente, mensaje):
        hilo = self.lista_hilos[cliente]
        hilo[1].put(mensaje)
       
    def crear_cola(self):
        cola_espera_in = queue.Queue()
        cola_espera_out = queue.Queue()
        return (cola_espera_in, cola_espera_out)    
        
    def obtener_cantidad_threads(self):
        thread_cantidad_inicial = threading.active_count()
        return thread_cantidad_inicial
    
    def hilo_esta_activo(self, hilo):
        return hilo.is_alive()        
    
    def imprimir_mensaje(self, mensaje):
        print (mensaje)        
    
    def finalizar_pool(self):
        for hilo in self.lista_hilos.values():
            print (hilo)
            hilo[0].join()
        print ("pool finalizada... Desconectando")

if __name__ == "__main__":
    pool_hilo_principal()
    