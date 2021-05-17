from plc import *
def socket(payload):
    if(payload == "rutina1"):
        Q4.Out("S")
        wait(2000)
        Q4.Out("R")
        wait(2000)
        return "This is the mesagge sended to client (1)"
        
    if(payload == "rutina2"):
        for i in range(10):
            Q4.Out("S")
            wait(100)
            Q4.Out("R")
            wait(100)
        return "This is the mesagge sended to client (2)"