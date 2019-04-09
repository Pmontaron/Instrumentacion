import visa 

class osciloscopio:
    
    
    def estado(self):   #Define la funcion estado
    
        # No logramos que conteste sin darle argumento a osciloscopio.estado
        def __init__(self,on_off):  #Define la propiedad on_off
            self.on_off=on_off
    
        rm = visa.ResourceManager()    # Devuelve todos los recursos conectados 
        a = rm.list_resources()    # arma una tupla con los instrumentos 
        #print(a)
        
    #Seleccionamos el instrumento 
        
        for i in range( 0 , len(a)):    # Selecciona un Osciloscopio
            if a[i][0:21]=='USB0::0x0699::0x0363:': # Seleccionamos elemento i desde caracter 0 al 20  y 'Conexion :: Fabricante :: Modelo :: Numero de serie'
                 on_off= 'on'  #Si encuentra el instrumento 
                 index = i
                 break
            else:
                 on_off = 'off'  # Si no encuentra el instrumento
                              
        return on_off , index # Devuelve si esta prendido o no
       
     
    def nombre(self):
         
        b=osciloscopio.estado(1)
        osc = rm.open_resource(a[b[1]])  # Abre el instrumento
        print(osc.query('*IDN?'))