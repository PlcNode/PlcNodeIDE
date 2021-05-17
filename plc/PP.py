
from machine import Pin
#------------------------------------------------------------------------------
class Entrada:
    '''Clase para entradas'''

    def __init__(self, pin, ent = 0):
        #Se introduce el pin y el modo de funcionamiento
        if ent == "PU":
            self.__I = Pin(pin, Pin.IN, Pin.PULL_UP)
        else:
            self.__I = Pin(pin, Pin.IN, Pin.PULL_DOWN)
        self.__preval = self.__I.value()
    
    def Res(self):
        '''Reset'''
        self.__preval = self.__value
        self.value = 0

    def leer(self, mode = 0):
        '''Funcion que retorna el valor y detecta flancos'''
        #Rising
        if mode == "Rising" and self.__preval == 0 and self.__I.value() == 1:
            self.__value = 1
        #Falling
        elif mode == "Falling" and self.__preval == 1 and self.__I.value() == 0:
            self.__value = 1
        #NO
        elif mode == "NO":
            self.__value = self.__I.value()
        #NC
        elif mode == "NC":
            self.__value = not self.__I.value()
        else:
            print("error")
            self.__value = self.__I.value()

    def Val(self):
        '''Funcion que lee el estado de las entradas'''
        return self.__value


class Salida:
    ''' Clase para salidas'''
    
    def __init__(self, pin, value = 0):
        #Se introduce el pin y un valor opcional de inicio
        if value in ("True", "On", 1):
            value = 1
        elif value in ("False", "Off", 0):
            value = 0
        else: pass
        #se crea el objeto
        self.__Q =  Pin(pin, Pin.OUT, value)

    def Res(self):
        '''Reset'''
        if not self.__value == 'S':
            self.Out("Off")
    
    def Out(self, state = "On"):
        '''Se almacena el estado deseado'''
        self.__value = state
        print(self.__value)
    
    def Set(self):
        '''Se ejecuta el estado deseado'''
        self.__Out()
    
    def __Out(self):
        '''Cambiar salida'''
        print(self.__value)
        #On
        if self.__value == "On":
            self.__Q.on()    
        #Off
        elif self.__value == "Off":
            self.__Q.off()
        #TOGGLE
        elif self.__value == 'T':
            if self.__Q.value == 1:
                self.__Q.off()
            elif self.__Q == 0:
                self.__Q.on()
        #Set
        elif self.__value == 'S':
            self.__Q.on()
        #Reset
        elif self.__value == 'R' or not self.__value.is_integer() or self.__value < 0 or self.__value > 4096:
            self.__Q.off()
        #PWM
        else:
            pass

    def Value(self):
        '''Consulta de valor actual'''
        return self.__Q.value()

def Reset():
    I0.Res()
    I1.Res()
    I2.Res()
    I3.Res()
    I4.Res()
    I5.Res()
    Q0.Res()
    Q1.Res()
    Q2.Res()
    Q3.Res()
    Q4.Res()
    Q5.Res()

def Leer():
    I0.leer()
    I1.Leer()
    I2.Leer()
    I3.Leer()
    I4.Leer()
    I5.Leer()

def Set():
    Q0.Set()
    Q1.Set()
    Q2.Set()
    Q3.Set()
    Q4.Set()
    Q5.Set()

I0 = Entrada(36)
I1 = Entrada(39)
I2 = Entrada(34)
I3 = Entrada(35)
I4 = Entrada(32)
I5 = Entrada(33)

Q0 = Salida(19,1)
Q1 = Salida(23,1)
Q2 = Salida(18,1)
Q3 = Salida(5,1)
Q4 = Salida(4,1)
Q5 = Salida(15,1)