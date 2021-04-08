
import machine
import ssd1306
import time
import network
import ujson
import plc
import plcsocket
import plcinterrupt

#------------------------------------------------------------------------------

data = ujson.loads(str('{"div_debug": ""}'))

# ----------------------------------------------------------------------------

class plcClass:

    def __init__(self):
        self.plcJson = self.deserialize(open("plc.json").read())
        self.socketPayload = ""

        self._Q0 = machine.Pin(23, machine.Pin.OUT)
        self._Q1 = machine.Pin(19, machine.Pin.OUT)
        self._Q2 = machine.Pin(18, machine.Pin.OUT)
        self._Q3 = machine.Pin(5, machine.Pin.OUT)
        self._Q4 = machine.Pin(4, machine.Pin.OUT)
        self._Q5 = machine.Pin(15, machine.Pin.OUT)

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
            payload = _plc.socketPayload
            _plc.socketPayload = ""
            try:
                plcsocket.socket(_plc ,payload)
            except:
                self.console_log("Error in plc socket")

            if ((time.ticks_ms()-currentTime)>float(delay)):
                break

    def console_log(self, string):
        try:
            data['div_debug'] = str(string)
        except:
            print(string)

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

    def Q0(self,state):
        if ((state == 1) or (state == True)):
            self._Q0.on()
        if ((state == 0) or (state == False)):
            self._Q0.off()
    def Q1(self,state):
        if ((state == 1) or (state == True)):
            self._Q1.on()
        if ((state == 0) or (state == False)):
            self._Q1.off()
    def Q2(self,state):
        if ((state == 1) or (state == True)):
            self._Q2.on()
        if ((state == 0) or (state == False)):
            self._Q2.off()
    def Q3(self,state):
        if ((state == 1) or (state == True)):
            self._Q3.on()
        if ((state == 0) or (state == False)):
            self._Q3.off()
    def Q4(self,state):
        if ((state == 1) or (state == True)):
            self._Q4.on()
        if ((state == 0) or (state == False)):
            self._Q4.off()
    def Q5(self,state):
        if ((state == 1) or (state == True)):
            self._Q5.on()
        if ((state == 0) or (state == False)):
            self._Q5.off()
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

_plc = plcClass()
print(_plc.freeMemory())

#-----------------------------------------------------------------------------------

i2c = machine.I2C(-1, scl=machine.Pin(22), sda=machine.Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

for i in range(5):
    oled.text('PlcNode', 28, 0)
    oled.text("V"+str(i), 56, 30)
    oled.show()
    oled.fill(0)
    time.sleep(.5)

# ----------------------------------------------------------------------------

try:
    plc.setup(_plc)
except:
    _plc.console_log("Error in plc setup")

#--------------------------------------------------------------------

wifiName = _plc.plcJson['wifiName']
wifiPassword = _plc.plcJson['wifiPassword']
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(wifiName, wifiPassword)

count = 0
pointers = "."

while not(station.isconnected()):
    oled.fill(0) # Clear display
    oled.text(wifiName, 8, 20)
    oled.text(wifiPassword, 8, 30)
    oled.text(pointers, 6, 40)
    oled.show()
    pointers = pointers + "."
    count = count + 1
    time.sleep(0.5)
    if pointers == "...................":
        pointers = ""
    if count == 50:
        station.active(False)
        break

oled.fill(0) # Clear display

if not(station.isconnected()):
    wifiName = 'PLCNODE'
    wifiPassword = 'NODEWIFI'
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=wifiName, password=wifiPassword)
    print(ap.ifconfig())
    oled.text(str(ap.ifconfig()[0]), 6, 40)
else:
    oled.text(str(station.ifconfig()[0]), 6, 40)
    
oled.text(wifiName, 8, 20)
oled.text(wifiPassword, 8, 30)
oled.show()

#-------------------------------------------------------------------------------

from microWebSrv import MicroWebSrv 

@MicroWebSrv.route('/')
def _httpHandlerTestGet(httpClient, httpResponse) :
	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = "text/html",
								  contentCharset = "UTF-8",
								  content 		 = open("index.html").read() )


# ----------------------------------------------------------------------------

def _acceptWebSocketCallback(webSocket, httpClient):
	print("WS ACCEPT")
	webSocket.RecvTextCallback   = _recvTextCallback
	webSocket.RecvBinaryCallback = _recvBinaryCallback
	webSocket.ClosedCallback 	 = _closedCallback

def _recvTextCallback(webSocket, msg):
    _plc.socketPayload = msg
    _data = _plc.deserialize(str(msg))
    if(_data['save'] == "True"):
        plc_py = open("plc.py","w")
        plc_py.write(_data['plc_py'])
        plc_py.close()
        plc_interrupt_py = open("plcinterrupt.py","w")
        plc_interrupt_py.write(_data['plc_interrupt_py'])
        plc_interrupt_py.close()
        plc_socket_py = open("plcsocket.py","w")
        plc_socket_py.write(_data['plc_socket_py'])
        plc_socket_py.close()
        div_html = open("div.html","w")
        div_html.write(_data['div_html'])
        div_html.close()
        plc_json = open("plc.json", "w")
        plc_json.write(_plc.serialize(_plc.plcJson))
        plc_json.close()
        machine.reset()
    if(_data['update'] == "True"):
        _data_ = ujson.loads(str('{"update": "", "updateTime": "", "autoScroll": "", "plc_py": "", "div_html":"", "plc_interrupt_py":"", "plc_socket_py": ""}'))
        _data_['update'] = "True"
        _data_['plc_py'] = open("plc.py").read()
        _data_['div_html'] = open("div.html").read()
        _data_['plc_interrupt_py'] = open("plcinterrupt.py").read()
        _data_['plc_socket_py'] = open("plcsocket.py").read()
        _data_['updateTime'] = _plc.deserialize(open("plc.json").read())['updateTime']
        _data_['autoScroll'] = _plc.deserialize(open("plc.json").read())['autoScroll']
        webSocket.SendText("%s" % str(_plc.serialize(_data_)))
        _data_['update'] = "False"
    if(_data['debug'] == "True"):
        _data_ = ujson.loads(str('{"debug":"", "div_debug": ""}'))
        _data_['debug'] = "True"
        _data_['div_debug'] = data['div_debug']
        webSocket.SendText("%s" % str(_plc.serialize(_data_)))

def _recvBinaryCallback(webSocket, data):
	print("WS RECV DATA : %s" % data)

def _closedCallback(webSocket):
	print("WS CLOSED")


srv = MicroWebSrv(webPath='www/')
srv.MaxWebSocketRecvLen     = 1024*30
srv.WebSocketThreaded		= True
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
srv.Start(True)

# ----------------------------------------------------------------------------

try:
    plcinterrupt.interrupts(_plc)
    _plc.I0Interrupt(interruptI0)
    _plc.I1Interrupt(interruptI1)
    _plc.I2Interrupt(interruptI2)
    _plc.I3Interrupt(interruptI3)
    _plc.I4Interrupt(interruptI4)
    _plc.I5Interrupt(interruptI5)
except:
    _plc.console_log("Error in plc interrupts")

# ----------------------------------------------------------------------------

thisTime1 = time.ticks_ms()

while True:
    payload = _plc.socketPayload
    _plc.socketPayload = ""
    plcsocket.socket(_plc ,payload)
    if( time.ticks_ms() - thisTime1 > 1):
        thisTime1 = time.ticks_ms()
        try:
            plc.loop(_plc)
        except:
            _plc.console_log("Program error")

#-----------------------------------------------------------------------------------

