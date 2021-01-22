# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 18:53:00 2018

@author: Hossam
Title: HP8156A optical attenuator class
"""

import rvisa as visa
import time

class HP8156A(object):
    
    def __init__(self,address):
        rm = visa.ResourceManager()
        self.inst = rm.open_resource(address)
        print(self.inst.ask("*IDN?"))
        
    def getPower(self):
        power=self.inst.query('FETC2:POW?')
        return float(power)
        
    