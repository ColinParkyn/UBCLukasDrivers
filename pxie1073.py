# -*- coding: utf-8 -*-
"""
Created on Thu Aug 03 15:02:38 2017

@author: nidaqmx
"""

import nidaqmx
import nidaqmx.system
system = nidaqmx.system.System.local()
system.driver_version

class pxie1073(object):

    def __init__(self,slot):
        self.slot = slot
        print('Connected to PXI')
#        self.voltage
           
    def setVoltage(self,ch,value):
        ch = int(ch-1)
#        print('pxiCH'+str(ch+1)+' = '+str(value)+'V')
        if (value<=10.0):
            with nidaqmx.Task() as task:
                task.ao_channels.add_ao_voltage_chan(self.slot+'/ao'+ str(ch))
                task.write([value], auto_start=True)
            self.voltage = value
        else:
            print('Voltage set to pxi is larger than the range!')
    
    def getVoltage(self, ch):
        return self.voltage