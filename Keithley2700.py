import rvisa as visa

class Keithley2700(object):
    # Define Class for LDC501
    def __init__(self):
        self.connected = False

    def __del__(self):
        if self.connected:
            self.disconnect()

    def connect(self, visaAddr):
        self.rm = visa.ResourceManager()
        self.instrument = self.rm.open_resource(visaAddr)
        print(self.instrument.query('*IDN?'))
        self.connected = True
        
    def getVoltage(self):
        print(self.instrument.query('SENSe1:FUNCtion VOLTage:DC'))

    def disconnect(self):
        self.instrument.close()
        
    def getVoltageZ(self):
        print 'hossam is supposed to read the voltage and return it'
        
