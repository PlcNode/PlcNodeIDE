from ejemplo import *
from plc import *

def setup():
    setWifiName("HOME-CF80")
    setWifiPassword("eslamisma0")

def loop():
    rutina1()
    Q0.Out()
    Q1.Out()
    Q2.Out()
    Q3.Out()