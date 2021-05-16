
import plc
import main
import ssd1306
import machine
import time
import network

plc = plc._plc()
# ----------------------------------------------------------------------------

print(plc.freeMemory())

#-----------------------------------------------------------------------------------

i2c = machine.I2C(-1, scl=machine.Pin(22), sda=machine.Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

for i in range(6):
    oled.text('PlcNode', 28, 0)
    oled.text("V"+str(i), 56, 30)
    oled.show()
    oled.fill(0)
    time.sleep(.5)

#--------------------------------------------------------------------

wifiName = plc.plcJson['wifiName']
wifiPassword = plc.plcJson['wifiPassword']
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(wifiName, wifiPassword)

count = 0
pointers = "."

while not(station.isconnected()):
    oled.fill(0)
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

oled.fill(0)

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

@MicroWebSrv.route("/")
def _httpHandlerTestGet(httpClient, httpResponse) :
    httpResponse.WriteResponseFile("/index.html", 
                                contentType="text/html", 
                                headers=None)

@MicroWebSrv.route("/manifest.json")
def _httpHandlerTestGet(httpClient, httpResponse) :
    httpResponse.WriteResponseFile("/manifest.json", 
                                contentType="text", 
                                headers=None)
                    
@MicroWebSrv.route("/data/files")
def _httpHandlerTestGet(httpClient, httpResponse) :
    httpResponse.WriteResponseOk(headers=None, 
                                contentType="text", 
                                contentCharset="UTF-8", 
                                content= plc.getContentFiles() )

@MicroWebSrv.route("/actions/delete_file", "POST")
def _httpHandlerTestPost(httpClient, httpResponse) :
    _data = httpClient.ReadRequestContentAsJSON()
    if _data['delete_file']==True:
        uos.remove(_data['file'])
        httpResponse.WriteResponseOk(headers=None, 
                                contentType="text", 
                                contentCharset="UTF-8", 
                                content= "Deleted file:"+_data['file']+"\n")

@MicroWebSrv.route("/actions/restart", "POST")
def _httpHandlerTestPost(httpClient, httpResponse) :
    _data = httpClient.ReadRequestContentAsJSON()
    httpResponse.WriteResponseOk(headers=None, 
                                contentType="text", 
                                contentCharset="UTF-8", 
                                content= "Restarted\n")
    if _data['restart']==True:
        timeNow = time.ticks_ms()
        while True:
            if (time.ticks_ms()-timeNow) > 1000:
                machine.reset()
    

@MicroWebSrv.route("/actions/save_files", "POST")
def _httpHandlerTestPost(httpClient, httpResponse) :
    _data = httpClient.ReadRequestContentAsJSON()
    print(_data)
    if _data['save_files']==True:
        for i in _data['files']:
            file = open('/'+i, "w")
            file.write(_data['files'][i])
            file.close()
        httpResponse.WriteResponseOk(headers=None, 
                                    contentType="text", 
                                    contentCharset="UTF-8", 
                                    content= "Saved\n")

# ----------------------------------------------------------------------------

def _acceptWebSocketCallback(webSocket, httpClient):
	print("WS ACCEPT")
	webSocket.RecvTextCallback   = _recvTextCallback
	webSocket.RecvBinaryCallback = _recvBinaryCallback
	webSocket.ClosedCallback 	 = _closedCallback

def _recvTextCallback(webSocket, msg):
    _data = plc.deserialize(str(msg))
    if _data['debug'] == True:
        if plc.lastSocketDebug != plc.socketDebug:
            webSocket.SendText("%s\n" % plc.socketDebug)
            plc.lastSocketDebug = plc.socketDebug

def _recvBinaryCallback(webSocket, data):
	print("WS RECV DATA : %s" % data)

def _closedCallback(webSocket):
	print("WS CLOSED")


srv = MicroWebSrv(webPath='www/')
srv.MaxWebSocketRecvLen     = 1024*10
srv.WebSocketThreaded		= True
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
srv.Start(True)

# ----------------------------------------------------------------------------

try:
    main.setup(plc)
except:
    plc.console_log("Error in setup")

thisTime1 = time.ticks_ms()



while True:
    if( time.ticks_ms() - thisTime1 > 1):
        thisTime1 = time.ticks_ms()
        try:
            main.loop(plc)
        except:
            plc.console_log("Program error")

#-----------------------------------------------------------------------------------

