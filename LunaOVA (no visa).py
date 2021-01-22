import subprocess
from numpy import *
import re

class LunaOVA():
    
    execLocation = 'C:/Users/Admin/Desktop/SendCmd.exe'
    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    
    def query(self, cmd):
        res = subprocess.check_output(self.execLocation+' "'+cmd+'" '+self.ip+' '+self.port)
        return res.replace('\x00', '').splitlines()[3:]
        
    def getRawJones(self):
        jonesData = self.query('FETC:JONE?')
        
        jones_a = zeros(len(jonesData), dtype=complex64)
        jones_b = zeros(len(jonesData), dtype=complex64)
        jones_c = zeros(len(jonesData), dtype=complex64)
        jones_d = zeros(len(jonesData), dtype=complex64)
        
      
        for ii in xrange(len(jonesData)):
            match = jonesData[ii].split('\t')

            jones_a[ii] = float(match[0])+1j*float(match[1]) 
            jones_b[ii] = float(match[2])+1j*float(match[3]) 
            jones_c[ii] = float(match[4])+1j*float(match[5]) 
            jones_d[ii] = float(match[6])+1j*float(match[7]) 
            
        return jones_a,jones_b,jones_c,jones_d
        
    def getGroupDelay(self):
        gdData = self.query('FETC:MEAS? 1')
        gd = asarray(map(float,gdData))
        return gd

    def getDispersion(self):
        dispData = self.query('FETC:MEAS? 2')
        disp = asarray(map(float,dispData))
        return disp        
        
    def getWavelength(self):
        wvlData = self.query('FETC:XAXI? 0')
        wvl = asarray(map(float,wvlData))
        return wvl  
        
    def getIL(self):
        ILData = self.query('FETC:MEAS? 0')
        IL = asarray(map(float,ILData))
        return IL 
        
    def getMeasDetails(self):
        return self.query('FETC:MDET?')
  
    def getJones(self):
        jonesDataAmp = self.query('FETC:MEAS? 7')
        jonesDataPhase = self.query('FETC:MEAS? 8')
        
        jones_a = zeros(len(jonesDataAmp), dtype=complex64)
        jones_b = zeros(len(jonesDataAmp), dtype=complex64)
        jones_c = zeros(len(jonesDataAmp), dtype=complex64)
        jones_d = zeros(len(jonesDataAmp), dtype=complex64)
        
      
        for ii in xrange(len(jonesDataAmp)):
            ampMatch = jonesDataAmp[ii].split('\t')
            phaseMatch = jonesDataPhase[ii].split('\t')
            jones_a[ii] = float(ampMatch[0])*exp(1j*float(phaseMatch[0]))
            jones_b[ii] = float(ampMatch[1])*exp(1j*float(phaseMatch[1]))
            jones_c[ii] = float(ampMatch[2])*exp(1j*float(phaseMatch[2]))
            jones_d[ii] = float(ampMatch[3])*exp(1j*float(phaseMatch[3]))
            
        return jones_a,jones_b,jones_c,jones_d