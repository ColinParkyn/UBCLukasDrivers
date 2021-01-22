# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 19:27:04 2018

@author: Hossam
Title: AQ6317B module for the 600-1750 nm OSA containing only 1 class
"""

import rvisa as visa
import time
import numpy as np

class AQ6317B(object):
    
    def __init__(self,address):
        rm = visa.ResourceManager()
        self.inst = rm.open_resource(address,timeout=100000)
        print(self.inst.ask("*IDN?"))
        
    def SingleSweep(self): # does a single sweep
        self.inst.query('SGL')
        
    def getStatus(self):
        status=self.inst.query('SWEEP?')
        status=str(status)
        status=status[:len(status)-2]
        return status

    def setStartWL(self,wavelength_nm): # set the center wavelength in nm
        self.inst.write('STAWL'+str(wavelength_nm))

    def setStopWL(self,wavelength_nm): # set the center wavelength in nm
        self.inst.write('STPWL'+str(wavelength_nm))
        
    def setCenterWL(self,wavelength_nm): # set the center wavelength in nm
        self.inst.write('CTRWL'+str(wavelength_nm))

    def setSpanWL(self,wavelength_span_nm): # set the span wavelength in nm
        self.inst.write('SPAN'+str(wavelength_span_nm))

    def setYscale(self,Yscale): # set the Yscale dB/div
        self.inst.write('LSCL'+str(Yscale))
        
    def setSensitivity(self,Sense): # set the sensitivity: SNHD, SNAT, SMID, SHI1, SHI2, SHI3
        self.inst.write(Sense)

    def setLSunit(self,unit): # set the level axis scale display between dBm and dBm/nm. Chose '0' for dBm and '1' for dBm/nm
        self.inst.write('LSUNT '+unit)

    def getLSunit(self): # gets the level axis scale display, either dBm and dBm/nm. Output is '0' for dBm/resolution and '1' for dBm/nm
        LSunit = self.inst.ask('LSUNT?')
        LSunit=str(LSunit)
        LSunit=LSunit[:len(LSunit)-2]
        return LSunit

    def getSense(self): # set the level axis scale displace between dBm and dBm/nm. Chose '0' for dBm and '1' for dBm/nm
        LSunit = self.inst.ask('SENSE?')
        LSunit=str(LSunit)
        LSunit=LSunit[:len(LSunit)-2]
        return LSunit

    def getRes(self): # set the level axis scale displace between dBm and dBm/nm. Chose '0' for dBm and '1' for dBm/nm
        LSunit = self.inst.ask('RESLN?')
        LSunit=str(LSunit)
        LSunit=LSunit[:len(LSunit)-2]
        return LSunit
        
    def getPower(self): # set the Yscale dB/div
        PWR=self.inst.query('LDATA')
        PWR=str(PWR) # convert from unicode to string
        PWR=PWR.split(',') # split at the delimiter and set as list
        last=PWR[len(PWR)-1] # select the last element
        last=last[:len(last)-2] # remove the last two characters in the string
        #last=np.asarray(last) # convert the last element to array
        PWR.pop(0) # remove first element
        PWR.pop() # remove last element
        #PWR=np.asarray(PWR) # convert to array
        PWR=np.append(PWR,last)
        PWR=map(float,PWR) # map the strings in the list to float
        PWR=np.array(PWR) # convert to array
        PWR=np.where(PWR==-210.0, -np.inf, PWR)
        return PWR
    
    def getWL(self): # wavelength data points
        WL=self.inst.query('WDATA')
        WL=str(WL) # convert from unicode to string
        WL=WL.split(',') # split at the delimiter and set as list
        last=WL[len(WL)-1] # select the last element
        last=last[:len(last)-2] # remove the last two characters in the string
        #last=np.asarray(last) # convert the last element to array
        WL.pop(0) # remove first element
        WL.pop() # remove last element
        #WL=np.asarray(WL) # convert to array
        WL=np.append(WL,last)
        WL=map(float,WL) # map the strings in the list to float
        WL=np.array(WL) # convert to array
        return WL
        
    def getStartWL(self):
        start=self.inst.query('STAWL?')
        return start
        
    def getStopWL(self):
        stop=self.inst.query('STPWL?')
        return stop
        
    def setResol(self,resolution): # set the resolution in nm
        self.inst.write('RESLN'+str(resolution))
        
    def setAvg(self,average): # set the resolution in nm
        self.inst.write('AVG'+str(average))