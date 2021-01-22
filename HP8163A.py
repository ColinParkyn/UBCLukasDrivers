# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 19:44:15 2018

@author: Hossam
Title: AQ6317B module for the 600-1750 nm OSA containing only 1 class
"""

import rvisa as visa
import time

class HP81531A(object):
    
    def __init__(self,address):
        rm = visa.ResourceManager()
        self.inst = rm.open_resource(address)
        print(self.inst.ask("*IDN?"))
        
    def getPower(self,slot):
        power=self.inst.query('FETC'+str(slot)+':POW?')
        return float(power)
        
    