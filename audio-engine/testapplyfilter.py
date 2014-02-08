#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Christophe
#
# Created:     25/01/2014
# Copyright:   (c) Christophe 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from datetime import datetime
import time
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal

class TestApplyfilter(object):
    """TestapplyFilter"""

    def __init__(self,wl):
        # wl: waveloader object
        self.wl=wl  # references waveloader object

    def applyFilter(self):
        nSample = int(self.wl.sRate/20)                     # nombre de sample a extraire: 1/20 de seconde
        ptr = 0                                     # index a partir duquel on extrait
        xaxis=np.arange(0,nSample)

        c0 = self.wl.data[ptr:ptr+nSample].astype(float)       # extract portion of data

        plt.plot(xaxis,c0 )                         # plot before normlalize
        plt.show()

        c0 = c0 / float(2**(self.wl.sWidth*8))              # normalize to 1.0

        plt.plot(xaxis,c0 ) # plot after normlalize
        plt.show()

        # design filter
        Nyq = self.wl.sRate/2.
        wp = [300./Nyq,500./Nyq]
        ws = [200./Nyq,600./Nyq]
        gp = 1.
        gs = 30.

        N, wn = signal.buttord(wp,ws,gp,gs) # gets order and window
        print "N=",N," wn=",wn

        b, a = signal.butter(N,wn,btype='bandpass') # get butterwoth filter
        print "b=",b," a=",a

        d1 = datetime.now()
        for i in range(0,99):
            sf = signal.lfilter(b, a, c0)
        delta = datetime.now() - d1
        print "delta=", delta.seconds,".",delta.microseconds

        plt.plot(xaxis,c0,'r',xaxis,sf,'g')
        plt.show()

        fft0 = np.fft.rfft(c0)
        fft1 = np.fft.rfft(sf)
        freqs =np.fft.rfftfreq(len(c0),d=1./float(self.wl.sRate))
        db0 = 10*np.log10(abs(fft0 + 1e-15))
        db1 = 10*np.log10(abs(fft1 + 1e-15))
        plt.plot(freqs,db0,'r',freqs,db1,'g' )

        plt.show()

    def applyFilter2(self):
        nSample = int(self.wl.sRate/20)                     # nombre de sample a extraire: 1/20 de seconde
        ptr = 0                                     # index a partir duquel on extrait
        xaxis=np.arange(0,nSample)

        c0 = self.wl.data[ptr:ptr+nSample].astype(float)       # extract portion of data

        c0 = c0 / float(2**(self.wl.sWidth*8))              # normalize to 1.0

        # design filter
        Nyq = self.wl.sRate/2.
        wp = [350./Nyq,450./Nyq]
        ws = [300./Nyq,500./Nyq]
        gp = 0.1
        gs = 32.

        #  scipy.signal.iirdesign(wp, ws, gpass, gstop, analog=False, ftype='ellip', output='ba')[source]

        b, a = signal.iirdesign(wp,ws,gp,gs)

        d1 = datetime.now()
        for i in range(0,99):
            #sf = signal.filtfilt(b, a, c0) #sf = signal.lfilter(b, a, c0)
            sf = signal.lfilter(b, a, c0)
        delta = datetime.now() - d1
        print "delta=", delta.seconds,".",delta.microseconds

        plt.plot(xaxis,c0,'r',xaxis,sf,'g')
        plt.show()

        fft0 = np.fft.rfft(c0)
        fft1 = np.fft.rfft(sf)
        freqs =np.fft.rfftfreq(len(c0),d=1./float(self.wl.sRate))
        db0 = 10*np.log10(abs(fft0 + 1e-15))
        db1 = 10*np.log10(abs(fft1 + 1e-15))
        plt.plot(freqs,db0,'r',freqs,db1,'g' )

        plt.show()