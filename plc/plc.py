

def setup(plc):
    plc.setWifiName("FAMILIA ORTIZ")
    plc.setWifiPassword("WIFINODE")

def loop(plc):
    plc.console_log("Hello world!!")
    plc.Q0(1)
    plc.wait(2000) #Delay in mseconds
    plc.Q0(0)
    plc.wait(2000)
    plc.Q1(1)
    plc.console_log(plc.I0())
    plc.wait(2000) #Delay in mseconds
    plc.Q1(0)
    plc.wait(2000)
    plc.Q2(1)
    plc.wait(2000) #Delay in mseconds
    plc.Q2(0)
    plc.wait(2000)
    plc.Q3(1)
    plc.wait(2000) #Delay in mseconds
    plc.Q3(0)
    plc.wait(2000)
