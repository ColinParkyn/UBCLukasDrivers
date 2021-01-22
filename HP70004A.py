import rvisa as visa
import time
import ast # library to parse the string returned by the RIN measurements

class HP70004A():
    
    def __init__(self):
        self.connected = False

    def __del__(self):
        if self.connected:
            self.disconnect()

    def connect(self,visaAddr):    
        self.rm = visa.ResourceManager()
        self.instrument = self.rm.get_instrument(visaAddr,timeout=100000)        
        print(self.instrument.ask("IDN?")) #Requests the device for identification
        self.connected = True
        
    def disconnect(self):
        self.instrument.close()

    def setStartFreq(self, val,unit):
        self.instrument.write('FA %g'%val+unit+';') 

    def setStopFreq(self, val,unit):
        self.instrument.write('FB %g'%val+unit+';')

    def setRINmarker(self, val,unit):
        self.instrument.write('MKRINSYS %g'%val+unit+';')

    def setVIDBW(self, val,unit): # minimum is 300HZ
        self.instrument.write('VB %g'%val+unit+';')
    
    def setRESBW(self, val,unit): # maximum is 3MHz
        self.instrument.write('RB %g'%val+unit+';')        
    
    def measureRIN(self):
        self.RIN=ast.literal_eval(self.instrument.ask('RIN?')) # parse the string into the laser, system, thermal, and shot RIN
        return self.RIN

#%% note:

# units used throughout can be 'HZ','KHZ','MHZ','GHZ', refer to page 36 of the 70900 programming manual
