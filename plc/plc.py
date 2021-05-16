
import machine
import time
import ujson
import uos
import gc

#------------------------------------------------------------------------------

class _plc():

    def __init__(self):
        self.plcJson = ujson.loads(open("plc.json").read())
        self.socketPayload = ""
        self.socketDebug = ""
        self.lastSocketDebug = ""

        self._Q1 = machine.Pin(19, machine.Pin.OUT)
        self._Q0 = machine.Pin(23, machine.Pin.OUT)
        self._Q2 = machine.Pin(18, machine.Pin.OUT)
        self._Q3 = machine.Pin(5, machine.Pin.OUT)
        self._Q4 = machine.Pin(4, machine.Pin.OUT)
        self._Q5 = machine.Pin(15, machine.Pin.OUT)

        self._Q0.on()
        self._Q1.on()
        self._Q2.on()
        self._Q3.on()
        self._Q4.on()
        self._Q5.on()

        self._I0 = machine.Pin(36, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self._I1 = machine.Pin(39, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self._I2 = machine.Pin(34, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self._I3 = machine.Pin(35, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self._I4 = machine.Pin(32, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self._I5 = machine.Pin(33, machine.Pin.IN, machine.Pin.PULL_DOWN)
        
    def freeMemory(self):
        gc.collect()
        F = gc.mem_free()
        A = gc.mem_alloc()
        T = F+A
        P = '{0:.2f}%'.format(F/T*100)
        return ('Total:{0} Bytes,  Free:{1} Bytes, ({2})'.format(T,F,P))
        
    def wait(self,delay):
        currentTime = time.ticks_ms()
        while True:
            if ((time.ticks_ms()-currentTime)>float(delay)):
                break

    def console_log(self,string):
        self.socketDebug = str(string)

    def listDir(self):
        listdir = []
        for i in uos.listdir():
            if not (i == "plc.py" or i == "manifest.json" or i == "plc.json" or i == "boot.py" or i == "microWebSrv.py" or i == "microWebSocket.py" or i == "ssd1306.py" or i == "index.html"):
                listdir.append(i)
        return listdir

    def getContentFiles(self):
        content = {}
        for i in self.listDir():
            content[str(i)] = open('/'+i).read()
        return self.serialize(content)

    def deserialize(self, data):
        return ujson.loads(str(data))

    def serialize(self, data):
        return ujson.dumps(data)

    def setWifiName(self, data):
        self.plcJson['wifiName'] = str(data)

    def setWifiPassword(self, data):
        self.plcJson['wifiPassword'] = str(data)
        
    def getWifiName(self):
        return self.plcJson['wifiName']

    def getWifiPassword(self):
        return self.plcJson['wifiPassword']

    def Q0(self, state = -1):
        if ((state == 1) or (state == True)):
            self._Q0.on()
        if ((state == 0) or (state == False)):
            self._Q0.off()
        return self._Q0.value()

    def Q1(self, state = -1):
        if ((state == 1) or (state == True)):
            self._Q1.on()
        if ((state == 0) or (state == False)):
            self._Q1.off()
        return self._Q1.value()

    def Q2(self, state = -1):
        if ((state == 1) or (state == True)):
            self._Q2.on()
        if ((state == 0) or (state == False)):
            self._Q2.off()
        return self._Q2.value()

    def Q3(self, state = -1):
        if ((state == 1) or (state == True)):
            self._Q3.on()
        if ((state == 0) or (state == False)):
            self._Q3.off()
        return self._Q3.value()

    def Q4(self, state = -1):
        if ((state == 1) or (state == True)):
            self._Q4.on()
        if ((state == 0) or (state == False)):
            self._Q4.off()
        return self._Q4.value()

    def Q5(self, state = -1):
        if ((state == 1) or (state == True)):
            self._Q5.on()
        if ((state == 0) or (state == False)):
            self._Q5.off()
        return self._Q5.value()

    def I0(self):
        return self._I0.value()
    def I1(self):
        return self._I1.value()
    def I2(self):
        return self._I2.value()
    def I3(self):
        return self._I3.value()
    def I4(self):
        return self._I4.value()
    def I5(self):
        return self._I5.value()

    def I0Interrupt(self, callback):
        self._I0.irq (trigger=Pin.IRQ_RISING, handler=callback)
    def I1Interrupt(self, callback):
        self._I1.irq (trigger=Pin.IRQ_RISING, handler=callback)
    def I2Interrupt(self, callback):
        self._I2.irq (trigger=Pin.IRQ_RISING, handler=callback)
    def I3Interrupt(self, callback):
        self._I3.irq (trigger=Pin.IRQ_RISING, handler=callback)
    def I4Interrupt(self, callback):
        self._I4.irq (trigger=Pin.IRQ_RISING, handler=callback)
    def I5Interrupt(self, callback):
        self._I5.irq (trigger=Pin.IRQ_RISING, handler=callback)

