#Here your code in python
def rutina1(plc):
    for i in range(4):
        plc.Q0(1)
        plc.wait(25)
        plc.Q0(0)
        plc.wait(25)