
def socket(plc, payload):
    if(payload == "rutina1"):
        plc.Q4(1)
        plc.wait(2000)
        plc.Q4(0)
        plc.wait(2000)
        return "This is the mesagge sended to client (1)"
    if(payload == "rutina2"):
        for i in range(10):
            plc.Q4(1)
            plc.wait(100)
            plc.Q4(0)
            plc.wait(100)
        return "This is the mesagge sended to client (2)"