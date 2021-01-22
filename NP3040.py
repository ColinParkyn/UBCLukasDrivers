# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 12:34:17 2018

@author: Hossam
"""

import rvisa as visa
import time
import numpy as np

class NP3040(object):
    
    def __init__(self,address):
        rm = visa.ResourceManager()
        self.inst = rm.open_resource(address)
        print(self.inst.ask("*IDN?"))
    
    def ON(self):
            self.inst.write('TEC:OUT 1')
            
    def OFF(self):
        self.inst.write('TEC:OUT 0')
        
    def setT(self,temp):
        self.inst.write('TEC:STEP 1')
        read=float(self.inst.query('TEC:SET:T?'))
        difference=round(temp-read,2)
        if difference>0:      
            self.inst.write('TEC:INC '+str(int(10*difference)))
        else:
            self.inst.write('TEC:DEC '+str(int(-10*difference)))
        
    def getT(self):
        temp=self.inst.query('TEC:T?')
        return float(temp)
