import rvisa as visa
import time


class HP8156Attenuator():
    
    def __init__(self):
        self.connected = False

    def __del__(self):
        if self.connected:
            self.disconnect()
 

    def connect(self,visaAddr):    
        self.rm = visa.ResourceManager()
        self.instrument = self.rm.open_resource(visaAddr)#need the "GPIB::" thingy        
        print(self.instrument.ask("*IDN?")) #Requests the device for identification
        self.connected = True
        
    def disconnect(self):
        self.instrument.close()
        
    def getAttenuation(self):
        return float(self.instrument.ask(':INP:ATT?'))
        
    def setAttenuation(self, att):
        self.instrument.write(':INP:ATT %g'%att)

    def getCalibration(self):
        return float(self.instrument.ask(':INP:OFFS?'))
        
    def setCalibration(self, att):
        self.instrument.write(':INP:OFFS %g'%att)
        
    def setOutputEnable(self, opt): # 0 for off and 1 for on
        self.instrument.write(':OUTP %g'%opt)
        
    def setOffset(self, offset):
        self.instrument.write(':INPut:OFFSet %g'%offset)

    def test(self,a):
        print("hi",a)