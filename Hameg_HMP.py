import rvisa as visa
import time

class Hameg_HMP():
    
    def __init__(self):
        self.connected = False

    def __del__(self):
        if self.connected:
            self.disconnect()
 
    
    def connect(self,visaAddr):    
        self.rm = visa.ResourceManager()
        self.instrument = self.rm.get_instrument(visaAddr)        
        print(self.instrument.ask("*IDN?")) #Requests the device for identification
        self.connected = True
        
    def disconnect(self):
        self.instrument.close()
        
    def setChannel(self, channel):
        self.instrument.write('INST:NSEL %d'%channel)
        self.checkError()

    def setVoltage(self, voltage, channel):
        
        self.setChannel(channel)
        self.instrument.write('VOLT %g'%voltage)
        self.checkError()
        
    def getVoltage(self, channel):
        
        self.setChannel(channel)
        res = self.instrument.ask('VOLT?')
        print res
        self.checkError()
        return float(res)
    
    def setCurrent(self, current, channel):
        
        self.setChannel(channel)
        self.instrument.write('CURR %g'%current)
        self.checkError()
        
    def getCurrent(self, channel):
        
        self.setChannel(channel)
        #res = self.instrument.ask('CURR?')
        res = self.instrument.ask('MEAS:CURR?')
        self.checkError()
        return float(res)
        
    def getErrorMessage(self):
        res = self.instrument.ask('SYSTem:ERRor?')
        return str(res)
        
    def checkError(self):
        e_str = self.getErrorMessage()
        e_num,e_msg = e_str.split(', ')
        if int(e_num) != 0:
            raise Exception(e_msg)
     
    def turnChannelOn(self,channel):
        self.setChannel(channel)
        res = self.instrument.write('OUTP ON')
        self.checkError()  
        
    def turnChannelOff(self,channel):
        self.setChannel(channel)
        res = self.instrument.write('OUTP OFF')
        self.checkError()
        