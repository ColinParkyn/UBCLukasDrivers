import rvisa as visa
import time
import ast
import numpy as np

class RS_FSW26():
    
    def __init__(self):
        self.connected = False

    def __del__(self):
        if self.connected:
            self.disconnect()
 
    def connect(self,visaAddr):    
        self.rm = visa.ResourceManager()
        self.instrument = self.rm.get_instrument(visaAddr,timeout=100000)        
        print(self.instrument.ask("*IDN?")) #Requests the device for identification
        self.connected = True
        
    def disconnect(self):
        self.instrument.close()

    # calibrate the RFSA
    def calibrate(self):
        self.instrument.write('*CAL?')
        
    # set resolution bandwidth    
    def setRESbw(self, freq,unit):
        self.instrument.write('BAND %d'%freq+' '+unit)

    # set video bandwidth    
    def setVIDbw(self, freq,unit):
        self.instrument.write('BAND:VID %d'%freq+' '+unit)

    # set start frequency    
    def setFREQstart(self, freq,unit):
        self.instrument.write('FREQ:STAR %d'%freq+unit)
        
    # set stop frequency    
    def setFREQstop(self, freq,unit):
        self.instrument.write('FREQ:STOP %d'%freq+unit)

    # set single sweep mode    
    def setSNGLsweep(self):
        self.instrument.write('INIT:CONT OFF')

    # set single sweep mode    
    def setSWPcount(self,count):
        self.instrument.write('SENS:SWE:COUN '+str(count))
        
    # initiate a new measurement and wait until the last sweep has finished
    def sweep(self):
        self.instrument.write('INIT;*WAI')
 
    # retrieve the RF spectrum      
    def getPWRspec(self, traceNO): # trace number can be from 1 to 4
        PWR = self.instrument.query('TRAC:DATA? TRACE'+str(traceNO)) # this is a unicode
        PWR=ast.literal_eval(PWR) # parses the unicode into elements in a tuple
        PWR=np.asarray(PWR) # convert the tuple to array
        return (PWR)

    def getFREQpts(self, traceNO): # trace number can be from 1 to 4
        FREQ = self.instrument.query('TRAC:X? TRACE'+str(traceNO)) # this is a unicode    
        FREQ=str(FREQ) # convert from unicode to string
        FREQ=FREQ.split(',') # split at the delimiter and set as list
        last=FREQ[len(FREQ)-1] # select the last element
        last=last[:len(last)-1] # remove the last two characters in the string '\n'
        FREQ[len(FREQ)-1]=last # replace the last element with the new string
        FREQ = map(float, FREQ) # map the strings in the list to float
        FREQ=np.array(FREQ) # convert the string to array
        return (FREQ)
        
    def getNdBdown(self):
        val = self.instrument.query('CALC:MARK:FUNC:NDBD:FREQ?') # this is a unicode    
        val=str(val) # convert from unicode to string
        val=val.split(',') # split at the delimiter and set as list
        last=val[len(val)-1] # select the last element
        last=last[:len(last)-1] # remove the last two characters in the string '\n'
        val[len(val)-1]=last # replace the last element with the new string
        val = map(float, val) # map the strings in the list to float
        val=np.array(val) # convert the string to array
        return (val)