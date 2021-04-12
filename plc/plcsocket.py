
def socket(plc, payload):
    if(payload == "rutina1"):
        plc.Q4(1)
        plc.wait(2000)
        plc.Q4(0)
        plc.wait(2000)
        return "This is the mesagge sended to client"