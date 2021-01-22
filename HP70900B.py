import rvisa as visa
import time
import ast # library to parse the string returned by the RIN measurements
import numpy as np

class HP70900B():
    
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

    def setSWEEPmode(self, swpmode): # 'SNGLS' is a single sweep mode
        self.instrument.write(swpmode+';') 

    def startSWEEP(self): # start sweeping
        self.instrument.write('TS;')
        
    def setVIDavg(self, val): # maximum is 3MHz
        self.instrument.write('VAVG %g'%val+';')   
        
    def getRIN(self):
        self.RIN=ast.literal_eval(self.instrument.ask('RIN?')) # parse the string into the RIN laser, RIN system, thermal, and shot terms
        return self.RIN

    def getAVGPWR(self): # measures the average power detected by the lightwave section
        self.AVGPWR=ast.literal_eval(self.instrument.ask('OPTPWR?')) # parse the string into the RIN laser, RIN system, thermal, and shot terms
        return self.AVGPWR

    def getRESPONSIVITY(self): # measures the responsovity of the PD in the lightwave section (in Volts/Watt)
        self.RSPSVTY=ast.literal_eval(self.instrument.ask('RSPSVTY?'))
        return self.RSPSVTY
        
    def getTRACE(self,traceLET): # traceLET refers to the trace letter
        self.TRACE=ast.literal_eval(self.instrument.ask('TR'+traceLET+'?')) # parse the string into array
        return self.TRACE
        
    def getF1(self): # measures the start frequency
        self.F1=ast.literal_eval(self.instrument.ask('FA?'))
        return self.F1
        
    def getF2(self): # measures the stop frequency
        self.F2=ast.literal_eval(self.instrument.ask('FB?'))
        return self.F2
        
    def getRB(self): # gets the set resolution bandwidth
        self.RB=ast.literal_eval(self.instrument.ask('RB?'))
        return self.RB
        
    def getRINmarker(self):
        self.RINmkr=ast.literal_eval(self.instrument.ask('MKRINSYS?')) # parse the string into the RIN laser, RIN system, thermal, and shot terms
        return self.RINmkr
        
#%% note:

# units used throughout can be 'HZ','KHZ','MHZ','GHZ', refer to page 37 of the 70900 programming manual