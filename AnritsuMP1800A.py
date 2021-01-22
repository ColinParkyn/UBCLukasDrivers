import rvisa as visa
import time


class AnritsuMP1800A():
    
    def __init__(self):
        self.connected = False

    def __del__(self):
        if self.connected:
            self.disconnect()
 

    def connect(self,visaAddr):    
        self.rm = visa.ResourceManager()
        self.instrument = self.rm.get_instrument(visaAddr)      
        self.instrument.read_termination = '\n'
        self.instrument.write_termination = '\n';
        
        print(self.instrument.ask('*IDN?')) #Requests the device for identification
        self.connected = True
        
    def disconnect(self):
        self.instrument.close()
        
    def startBER(self):
        # Wavelength must be in meters
        self.instrument.write(':SENS:MEAS:STAR')
        
    def stopBER(self):
        # Wavelength must be in meters
        self.instrument.write(':SENS:MEAS:STOP')
        
    
    def isBERrunning(self):
        # Wavelength must be in meters
        return int(self.instrument.ask(':SENSe:MEASure:EALarm:STATe?'))
    
    def getUnitNumber(self):
        return int(self.instrument.ask(':UENTry:ID?'))
        
        
    def setUnitNumber(self, unit):
        self.instrument.write(':UENTry:ID %d'%unit)
        
        
    def getModuleNumber(self):
        return int(self.instrument.ask(':MODule:ID?'))
        
        
    def setModuleNumber(self, unit):
        self.instrument.write(':MODule:ID %d'%unit)
        
                
    def getPortNumber(self):
        return int(self.instrument.ask(':PORT:ID?'))
        
        
    def setPortNumber(self, unit):
        self.instrument.write(':PORT:ID %d'%unit)
        
    def setInterfaceNumber(self, interface):
        self.instrument.write(':INTerface:ID %d'%interface)
        
        
    def getErrorRate(self):
        res = self.instrument.ask(':CALCulate:DATA:EALarm? "CURRent:ER:TOTal"')
        try:        
            ber = float(res.replace('"', ""))
        except ValueError:
            ber = 1
        return ber
        
    def setMeasPeriodUnit(self, unit):
        # Unit TIME, CLOCk, ERRor, BLOCk
        self.instrument.write(':SENSe:MEASure:EALarm:UNIT %s'%unit)
        
    def setMeasClockCount(self, count):
        # Set count to E_3, for 1e3, E_12 for 1e12 etc...
        self.instrument.write(':SENSe:MEASure:EALarm:CLOCkcnt %s'%count)
     
    def setMeasTime(self, time):
        # <day>,<hour>,<min>,<second> 
        self.instrument.write(':SENSe:MEASure:EALarm:PERiod %s'%time)   
    
        
    def setMeasMode(self, mode):
        # Mode set to REPeat, SINGle, UNTimed
        self.instrument.write(':SENSe:MEASure:EALarm:MODE %s'%mode)
        
    def getDataThreshold(self):
        return float(self.instrument.ask(':INPut:DATA:THReshold? DATA'))
        
    def getResultThreshold(self):
        res =  (self.instrument.ask(':CALCulate:DATA:EALarm? "CURRent:Threshold"'))
        return float(res[1:6])
        
    def setDataThreshold(self, threshold):
        self.instrument.write(':INPut:DATA:THReshold DATA, %.3f'%threshold)
        
    def setInputClockSelection(self, clkselection):
        #EXTernal or RECovered
        #write get method
        self.instrument.write(':INPut:CLOCk:SELection %s'%clkselection)
        
    def setAutoSearch(self, automode, channel):
        #FINE COARse
        self.instrument.write(':SYSTem:CFUNction ASE32') #AADJ for auto adjustment 
        print 'CFUNCTION=', self.instrument.ask(':SYSTem:CFUNction?')  
        self.instrument.write(':SENSe:MEASure:ASEarch:SLAReset') #all slots off
        self.instrument.write(':SENSe:MEASure:ASEarch:SMODe %s'%automode)
        print 'Auto Search Mode =', (self.instrument.ask(':SENSe:MEASure:ASEarch:SMODe?'))
        self.instrument.write(':SENSe:MEASure:ASEarch:MODE PHASe') #THReshold,  PTHReshold PHASe
        print 'Search for =', self.instrument.ask(':SENSe:MEASure:ASEarch:MODE?')
        self.instrument.write(':SENSe:MEASure:ASEarch:SELSlot SLOT4,%s'%channel,',ON')
        #print 'SLOT=',  self.instrument.ask(':SENSe:MEASure:ASEarch:SELSlot?')
    
    def setCFUOff(self):
        self.instrument.write(':SYSTem:CFUNction OFF') #AADJ for auto adjustment 
        print 'CFUNCTION=', self.instrument.ask(':SYSTem:CFUNction?')
    
    def startAutoSearch(self):
        self.instrument.write(':SENSe:MEASure:ASEarch:STARt');
    
    def isAutoSearchRunning(self):
        return int(self.instrument.ask(':SENSe:MEASure:ASEarch:STATe?'))
    
    def stopAutoSearch(self):
        self.instrument.write(':SENSe:MEASure:ASEarch:STOP')
        
    def stopAutoAdj(self):
        self.instrument.write(':SENSe:MEASure:AADJust:STOP')
    
    def isAutoAdjRunning(self):
        return int(self.instrument.ask(':SENSe:MEASure:AADJust:STATe?'))
        
    def setOutputDataRate(self, datarate):
        self.instrument.write(':OUTPut:DATA:BITRate %0.6f'%datarate)
        print 'BIT Rate =', self.getOutputDataRate(), 'Gb/s'    
        
    def getOutputDataRate(self):
        return float(self.instrument.ask(':OUTPut:DATA:BITRate?'))
        
    def calibrateDataOutput(self):
        self.instrument.write(':OUTPut:DATA:PCALibration')
        
        
    def relativeDelayToggle(self, toggle):
        # toggle ON or OFF
        self.instrument.write(':OUTPut:DATA:RELative %s'%toggle)
        
    
    def setRelativeDelay(self, delay):
        # delay in units of mUI
        self.instrument.write(':OUTPut:DATA:RDELay %d,UI'%delay)    
        
    def calibrateEDClock(self):
        #doesnt work
        self.instrument.write(':INPut:CLOCk:CALibration')
    
    #def getAutoSearchMode(self):
        #FINE COARse
        #print (self.instrument.ask(':SENSe:MEASure:ASEarch:SMODe?'))
        #self.instrument.ask(':SENSe:MEASure:ASEarch:MODE PTHReshold')
        #self.instrument.ask(':SENSe:MEASure:ASEarch:SELSlot SLOT4,%s'%channel,',ON')
        
   #:SENSe:MEASure:ASEarch:SLAReset
    #def setAutoSearchThPhMode(self, thpr):
        #FINE COARse
    #    self.instrument.write(':SENSe:MEASure:ASEarch:SMODe %s'%automode)
        
        
    
    
        
        