# -*- coding: utf-8 -*-
"""
Created on Tue Mar 05 10:01:47 2019

@author: Admin
"""
import rvisa as visa
import time
import numpy as np

class N7744A(object):
    
    def __init__(self,address):
        rm = visa.ResourceManager()
        self.inst = rm.open_resource(address)
        print(self.inst.ask("*IDN?"))

    def readPower(self,slot):
        power=self.inst.query('read'+str(slot)+':pow?')
        return float(power)
