# script modified by Hossam Shoman @ 1312 on the 17th of March 2017 from N7711A to N7714A

import rvisa as visa
import time


class N7714A(object):
    # Define class for Keysight N7711A laser
    def __init__(self,source):
        self.connected = False
        self.source = source # Source can be 1 to 4

    def __del__(self):
        if self.connected:
            self.disconnect()

    def connect(self, visaAddr):
        # Connects to the laser device
        self.rm = visa.ResourceManager()
        self.instrument = self.rm.open_resource(visaAddr)
        print(self.instrument.query("*IDN?"))
        self.connected = True

    def disconnect(self):
        self.instrument.close()

    def setPowerUnit(self, unit):
        # Unit can be DBM or W for watt
        self.instrument.write('SOUR{}:POW:UNIT {}'.format(self.source,unit))
        self.checkError()
        self.waitUntilDone()

    def setLaserState(self, state):
        # Turns the laser on and off. State can be on or off
        self.instrument.write('SOUR{}:POW:STAT {}'.format(self.source,state))
        self.checkError()
        self.waitUntilDone()

    def setLaserPower(self, power, unit):
        # Power units: DBM, MW
        self.instrument.write('SOUR{}:POW {}{}'.format(self.source,power,unit))
        self.checkError()
        self.waitUntilDone()

    def setGridMode(self, state):
        # Turns grid mode on or off
        self.instrument.write('SOUR{}:WAV:AUTO {}'.format(self.source,state))
        self.checkError()
        self.waitUntilDone()

    def setWavelength(self, wav):
        # Sets laser wavelength
        # Units: nm
        self.instrument.write('SOUR{}:WAV:CW {} nm'.format(self.source,wav))
        self.checkError()
        self.waitUntilDone()

    def readWavelength(self):
        # Read laser wavelength
        # units: nm
        return float(self.instrument.query('SOUR{}:WAV:CW?'.format(self.source)))*1E9

    def setLaserFreqGridOff(self, freq):
        # Sets the laser frequency when grid mode is off
        # units: Hz
        self.instrument.write('SOUR{}:FREQ {} Hz'.format(self.source,freq))
        self.checkError()
        self.waitUntilDone()

    def setGridRefFreq(self, freq):
        # Sets the reference frequency for grid mode
        # Units: Hz
        self.instrument.write('SOUR{}:FREQ:REF {} Hz'.format(self.source,freq))
        self.checkError()
        self.waitUntilDone()

    def setGridModeFreqOffset(self, offset):
        # Sets the frequency offset from the reference frequency while in grid mode
        # Units: Hz
        self.instrument.write('SOUR{}:FREQ:OFFS {} Hz'.format(self.source,offset))
        self.checkError()
        self.waitUntilDone()

    def setGridModeChan(self, chan):
        #
        self.instrument.write('SOUR{}:FREQ:CHAN {}'.format(self.source,chan))
        self.checkError()
        self.waitUntilDone()

    def checkError(self):
        errStr = self.instrument.ask('SYST:ERR?')
        res = int(errStr.split(',')[0])
        message = errStr.split(',')[1]
        print (message)
        if res:
            raise InstrumentError(message)

    def checkStatus(self):
        print(self.instrument.ask('*STB?'))

    def waitUntilDone(self):
        while int(self.instrument.ask('*OPC?')) == 0:
            time.sleep(0.25)


class InstrumentError(Exception):
    pass;

if __name__ == "__main__":
    ins = N7711A_august_24(1)
    ins.connect('USB0::0x0957::0x3718::MY50701193::INSTR')