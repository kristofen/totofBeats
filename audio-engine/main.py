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

import sys
import numpy as np
from waveloader import *
from generator import *
from testapplyfilter import *
from mixer import *
from bluetoothserver import *
from bluetoothclient import *
from commandprocessor import *
from configurationmanager import *
import matplotlib.pylab as plt

def main(file):

##    wl = WaveLoader('signal400.wav')
##    wl.open()
##    test = TestApplyfilter(wl)
##    test.applyFilter2()


##    buff=None
##    nb=44100*2*4
##    iteration=int(nb/1024)
##    debug=[]
##    lasttrace=False
##    dbgitem=None
##    for i in range(iteration):
##        lasttrace = Generator.trace
##        Generator.trace=(i>=85 and i<105) or (i>=170 and i<190) or (i>=255 and i<275)
##        if lasttrace==True and Generator.trace==False:
##            debug.append(dbgitem)
##            dbgitem=None
##        ret = g.needSamples(1024,None)
##        if ret is not None and Generator.trace:
##            if dbgitem is None:
##                dbgitem=ret
##            else:
##                dbgitem=np.vstack((dbgitem,ret))
##
##    #np.savetxt('test.out', debug, delimiter=',',fmt='%4f')   # X is an array
##    for i,v in enumerate(debug):
##        plt.plot(v[:,0])
##        plt.show()
##
##    return

    confMan = ConfigurationManager(file)
    confMan.load()

    for trk in confMan.conf['kits'][0]['tracks']:
        print trk['file']


    g = Generator(Mixer.sRate,Mixer.nbChannel,confMan)

    Mixer.registerGenerator(g)

    Mixer.start()  # starts audio mixer for output

    bt = BluetoothServer() # allocate bluetooth server
    bt.open(1) # open it

    try:
        mustStop=0
        while (mustStop==0):
            csock = bt.acceptConnection()  # block until a new bluetooth connection is made
            print "new connection bluetooth client"
            btc = BluetoothClient(csock) # allocates bluetooth client
            cp = CommandProcessor(g) # allocate object that will process commands from bluetooth clients
            btc.registerProcessor(cp)   # registers object that will process commands to the bluetooth client
            btc.registerBtServer(bt) # registers bluetooth server to client
            bt.registerNewConnection(btc) # registers client to server
            print "starting btclient"
            btc.start() # starts processing commands from bluetooth channel

    except:
        print "Unexpected error:", sys.exc_info()[0]

    bt.closeClients() # tells bt server to close all clients
    bt.close() # closes bt server
    Mixer.stop() # stop audio output mixer

    pass

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "USAGE: main conffile"
    else:
        print "conffile=",sys.argv[1]
        main(sys.argv[1])

