#-------------------------------------------------------------------------------
# Name:        Client Bluetooth
# Purpose:
#
# Author:      Christophe
#
# Created:     26/01/2014
# Copyright:   (c) Christophe 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys
import bluetooth
import threading
import time

class BluetoothClient(object):
    """BluetoothClient"""

    def __init__(self,csock):
        self.sock=csock
        self.t=None

    def registerProcessor(self,proc):
        self.commandProcessor = proc
        self.commandProcessor.registerClient(self)

    def start(self):
        print "BluetoothClient.start"
        #this is a comment
        try:
            self.t = threading.Thread(target=BluetoothClient.callback,args=(self,),name="bntcclient")
            self.mustStop=0
            self.isActive=False
            self.t.start()
        except:
            print "Unexpected error:", sys.exc_info()[0]," ", sys.exc_info()[1]," ", sys.exc_info()[2]

    @staticmethod
    def callback(btc):
        print "Bluetoothclient start thread"
        try:
            btc.isActive=True
            while (btc.mustStop==0):
                data = btc.sock.recv(1024)
                mustExit = btc.commandProcessor.bufferize(data)
                if mustExit:
                    btc.mustStop=1

        except:
            print "Unexpected error:", sys.exc_info()
        btc.isActive=False
        print "Bluetoothclient end of thread callback, btcmuststop=",btc.mustStop

    def registerBtServer(self,bt):
        self.btServer=bt

    def sendCommand(self,data):
        print "BluetoothClient send data=(",data,")"
        self.sock.send(data+'\r\n')


    def close(self):
        print "Bluetoothclient close"
        self.mustStop=1
        nbretry=0
        if self.t is not None:
            #on arrete le thread
            while (nbretry<25 and self.t.isAlive):
                #ccc
                time.sleep(0.250)
                nbretry += 1
            if self.t.isAlive:
                self.t = None
        self.sock.close()
        self.btServer.removeclient(self)
