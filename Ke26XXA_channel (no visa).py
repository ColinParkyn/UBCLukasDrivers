# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 00:07:08 2015

@author: Admin
"""
import numpy as np;
from scipy.interpolate import interp1d
from scipy.io import loadmat

class Ke26XXA_channel(object):
    name = 'Keithley 26xxA channel' #better name would have been ring heater
        
    def __init__(self, keith, channel, vmin, vmax, ringtype, poffset=5e-3, NPLC = 1.0, current_limit=100.0e-3, name = 'IRPH'):
        self.keithley = keith;
        self.ch = channel;
        self.vmin = vmin;
        self.vmax = vmax;
        self.ringtype = ringtype;
        self.current_limit = current_limit;
        
        self.lambda0_res = 1550e-9;
        self.poffset = poffset;
        
        self.keithley.setCurrentMeasurementRange(self.ch, self.current_limit)
        self.keithley.setAutoZeroMode(self.ch, 'auto')
        self.keithley.setNPLC(self.ch, NPLC);
        self.name = name;
        self.resdatafile = 'C:/Users/Admin/Desktop/Hasitha/sep2017/opsisvernier_fsrs.mat'
        
        
    def setCalibration(self, heaterX1, heaterX2, IVfunc3D):
        self.heaterX1 = heaterX1;
        self.heaterX2 = heaterX2;
        self.IVfunc3D = IVfunc3D;
        
    def getPDCurrent(self):
        current = self.getCurrent();
        voltage = self.getVoltage();
        voltageX1 = self.heaterX1.getVoltage();
        voltageX2 = self.heaterX2.getVoltage();
        iPD = current - self.IVfunc3D(voltage, voltageX1, voltageX2);
        return iPD
        
    def setCalibration2d(self, heaterX1, IVfunc2D):
        self.heaterX1 = heaterX1;
        self.IVfunc2D = IVfunc2D;
        
    # Sets the voltage for a channel. If cvMode is true sets channel automatically to constant voltage mode
    def setVoltage(self, voltage):
         #self.keithley.setVoltage(self.ch, voltage)
        if(voltage > self.vmax + 0.1): 
            print 'voltage larger than maximum channel voltage'
            self.keithley.setVoltage(self.ch, self.vmax)
        elif( voltage < 0.05):
            print 'voltage too small'
            self.keithley.setVoltage(self.ch, self.vmin)                
        else:
            self.keithley.setVoltage(self.ch, voltage)
            
    def setCurrent(self, current):
        self.keithley.setCurrent(self.ch, current)
            
    def setPower(self, power, vstep=0.01, power_accuracy = 0.1e-3):
        voltage = self.getVoltage()
        current = self.getCurrent()
        curr_power = voltage*current;
        
        if(curr_power < power):
            low_side = True
        else:
            low_side = False
            vstep = vstep*(-1.0)
        
        while(abs(power-curr_power) > power_accuracy):
            voltage = voltage + vstep
            self.setVoltage(voltage)
            
            voltage = self.getVoltage()
            current = self.getCurrent()
            curr_power = voltage*current;
            
            print str(curr_power*1e3) + 'mW     ' +  str(vstep)
            
            if(curr_power > power and low_side):
                vstep = vstep*(-1.0)
                vstep = vstep/2;
                low_side = False
                
            if(curr_power < power and low_side == False):
                vstep = vstep*(-1.0)
                vstep = vstep/2;
                low_side = True
                
            if(abs(vstep) < 1.0e-4):
                print 'Minimum voltage step reached without meeting power accuracy'
                break;

    def getVoltage(self):
        return self.keithley.getVoltage(self.ch)
        
    def getCurrent(self):
        return self.keithley.getCurrent(self.ch)
    
    #call to self populate IV curves
    def getIV(self, numPts=51):
        #numPts = 101;\
        voltages = np.linspace(self.vmin, self.vmax, numPts)
        currents = np.zeros(np.shape(voltages))
        
        v0 = self.getVoltage();
        self.setVoltage(self.vmin)
        
        for ii, VV in enumerate(voltages):
            self.setVoltage(VV)
            voltages[ii] = self.getVoltage()
            currents[ii] = self.getCurrent()
        
        self.setVoltage(v0)
        
        self.IVfunc = interp1d(voltages, currents.T, kind='cubic')
        power = voltages*currents;
        self.VPfunc_private = interp1d(power, voltages.T, kind = 'cubic', fill_value=self.vmin)
        
        self.pmin = power.min()
        self.pmax = power.max()
        return (voltages, currents)

    #to avoid out of range values
    def VPfunc(self, powervals):
        powervals = np.array(powervals)
        powervals[powervals < self.pmin] = self.pmin;
        powervals[powervals > self.pmax] = self.pmax;
        
        return self.VPfunc_private(powervals)
        
    def loadresdata(self):
        resdata = loadmat(self.resdatafile, squeeze_me=True, struct_as_record=False);
        return resdata     
        
    #find initial resonance locations    
    def calibrateResonances(self, lambda_cal_vec, p_res_vec):
        c_speed = 299792458.0;
        #get FSR: this to be replaced by propower matrix functions
        resdata = self.loadresdata()
        fsrs = resdata['fsr'+str(self.ringtype)+'_freq']
        lambda_reses = resdata['lambda_reses'+str(self.ringtype)]
        freq_reses = c_speed/lambda_reses
        pp = np.polyfit(freq_reses, fsrs, 1)
        fsrfunc = np.poly1d(pp)
        
        ## power requied to shift unit-phase
        pp = np.polyfit(p_res_vec, lambda_cal_vec, 1)
        p_res_func = np.poly1d(pp);
        lambda0_res = p_res_func(self.poffset)
        dP = 5e-3;
        lambda_dP = p_res_func(self.poffset + dP)
        
        dfreq = abs(c_speed/lambda0_res - c_speed/lambda_dP);
        
        dPhi = 2*np.pi*dfreq/fsrfunc(c_speed/lambda0_res)
        dP_dPhi = (dP)/dPhi
        
        ## calculate initial resonance locaitons
        freq0_res = c_speed/lambda0_res
        freq0_reses = freq0_res + np.arange(-5, 6)*fsrfunc(freq0_res) 
        lambda0_reses = c_speed/freq0_reses   
        
        #new calibrated variables 
        self.fsrfunc = fsrfunc
        self.p_res_func = p_res_func
        self.lambda0_reses = lambda0_reses
        self.dP_dPhi = dP_dPhi
       
    #return required power to tune the nearest resonance to lambda
    def getRequiredP(self, lambda_tuning):
        c_speed = 299792458.0;
        #idx = (abs(self.lambda0_reses[self.lambda0_reses < lambda_tuning] - lambda_tuning)).argmin();
        lambda_res = self.lambda0_reses[self.lambda0_reses < lambda_tuning].max()
        print lambda_res
        freq_res = c_speed/lambda_res
        print freq_res
        
        dphi_required = 2*np.pi*(freq_res - c_speed/lambda_tuning)/self.fsrfunc(c_speed/lambda_tuning)
        p_required = self.dP_dPhi*dphi_required + self.poffset
        
        return p_required
        
        
    
