import serial
import serial.tools.list_ports
import threading
from time import sleep
def findPort():
    ports = serial.tools.list_ports.comports(include_links=False)
    for port in ports :
        if "PI USB to Serial" in port.description:
            return port

class RfidReader:
    def __init__(self, eventHandler):
        self.port = findPort()

    def connect(self):
        self.reader = serial.Serial(
                        port=self.port.device,
                        baudrate= 9600,
                        parity = serial.PARITY_NONE,
                        stopbits = serial.STOPBITS_ONE,
                        bytesize = serial.EIGHTBITS,
                        timeout=1)

    def readTag(self):
        data = self.reader.readline().decode()
        if len(data) < 1:
            return None
        else:
            return data

