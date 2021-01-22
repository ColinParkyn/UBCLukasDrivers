import rvisa as visa
import time
from numpy import *
import numpy 

class Ke26XXA_tsp(object):
    
    def __init__(self, visaAddr):
        self.rm = visa.ResourceManager()
        self.instr = self.rm.get_instrument(visaAddr)      
        
#        self.reset('a')
#        self.reset('b')        
        self.instr.write('smua.nvbuffer1.clear()')
        self.instr.write('smub.nvbuffer1.clear()')
        self.instr.write('smub.nvbuffer1.appendmode = 0')
        self.instr.write('smua.nvbuffer1.appendmode = 0')
#        self.instr.values_format.container = numpy.array
#        self.instr.values_format.separator = ','
        self.instr.chunk_size = 102400
        
        print(self.instr.ask('*IDN?\n')) #Requests the device for identification
        self.instr.clear()
        
    def disconnect(self):
        self.instr.close()
        
    def connect(self, visaAddr):
        pass
    
    def sweepVmeasureI(self, ch, v1, v2, numPts = 101, delay = 1e-3):
        voltages = linspace(v1, v2, numPts)
                    
        try:
            self.instr.clear()
            self.instr.write('smu' + ch + '.nvbuffer1.clear()')
            self.instr.write('smu' + ch + '.nvbuffer1.appendmode = 0')
    #            self.instr.write('smu' + ch + '.nvbuffer1.capacity = ' + str(numPts))
    #        self.instr.write('smu' + ch + 'nvbuffer1.collectsourcevalues = 1')
            self.outputEnable(ch, True)  
            self.instr.write('SweepVLinMeasureI(smu' + ch +', ' + str(v1) 
                                    + ',' +str(v2) + ',' + str(delay) +', ' + str(numPts) + ')')
            time.sleep(delay*numPts)
            self.instr.write('waitcomplete()') 
            self.instr.write('printbuffer(1, ' + str(numPts) + ', smu' + ch + '.nvbuffer1.readings)')
            data = self.instr.read().split(',')
    
    
            self.outputEnable(ch, True)           
            self.instr.write('smu' + ch + '.nvbuffer1.clear()')
            self.instr.clear()
            cur = []
            for val in data:
                cur.append(float(val))
    #        
            return  array(cur), voltages
        except:
            self.instr.read()
            self.instr.write('smu' + ch + '.nvbuffer1.clear()')
            print 'sweep failed'
            return voltages*0.0, voltages
        
    # Sets the voltage for a channel. If cvMode is true sets channel automatically to constant voltage mode
    def setVoltage(self, chan, v, cvMode=True):
        self.instr.write('smu' + chan + '.source.levelv = ' + str(v))     
#        return self.instr.read()
        
    def getVoltage(self, chan):
        self.instr.write('print(smu' + chan + '.measure.v( ))')  
        return float(self.instr.read())
    
    def reset(self, chan):
        self.instr.write('smu' + chan + '.reset()' )
    
    # Sets the current for a channel. If ccMode is true sets channel automatically to constant current mode
    def setCurrent(self, chan, c, ccMode=True):
        self.instr.write('smu' + chan + '.source.leveli = ' + str(c)) 
        
    def getCurrent(self, chan):
        self.instr.write('print(smu' + chan + '.measure.i( ))')
        return float(self.instr.read())
    
    def setVoltageAutorange(self, chan, val):
        if val:
            self.instr.write('smu' + chan + '.measure.autorangev = smu' + chan + '.AUTORANGE_ON')
        else:
            self.instr.write('smu' + chan + '.measure.autorangev = smu' + chan + '.AUTORANGE_OFF')
            
        
    def setCurrentAutorange(self, chan, val):
        if val:
            self.instr.write('smu' + chan + '.measure.autorangei = smu' + chan + '.AUTORANGE_ON')
        else:
            self.instr.write('smu' + chan + '.measure.autorangei = smu' + chan + '.AUTORANGE_OFF')
            
            
    def setCurrentMeasurementRange(self, chan, val):
        self.setCurrentAutorange(chan, False)
        self.instr.write('smu' + chan + '.measure.rangei = ' + str(val))
    
    # Sets mode to be constant current ('cc') or constant voltage ('cv')        
    def setMode(self,chan,mode):
        if mode == 'cv':
            self.instr.write('smu' + chan + '.source.func = smu' + chan + '.OUTPUT_DCVOLTS')
        if mode == 'cc':
            self.instr.write('smu' + chan + '.source.func = smu' + chan + '.OUTPUT_DCAMPS')
     
    #set the auto zero function of the DAC  smua.AUTOZERO_OFF|smua.AUTOZERO_AUTO|smua.AUTOZERO_ONCE 
    def setAutoZeroMode(self, chan, mode):
        pass
    
    # Sets the integration time in number of power line cycles. Range 0.001 to 25 
    def setNPLC(self, chan, val):
        self.instr.write('smu' + chan + '.measure.nplc = ' + str(val))
    
    def outputEnable(self, chan, enable):
        if enable:
            self.instr.write('smu' + chan + '.source.output = smu' + chan + '.OUTPUT_ON')
        else:
            self.instr.write('smu' + chan + '.source.output = smu' + chan + '.OUTPUT_OFF')
    
    def setVoltageLimit(self, chan, val):
        self.instr.write('smu' + chan + '.source.limitv=' + str(val))
            
    def setCurrentLimit(self, chan, val):
        self.instr.write('smu' + chan + '.source.limiti=' + str(val))