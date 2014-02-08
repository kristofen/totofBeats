#-------------------------------------------------------------------------------
# Name:        Serveur Bluetooth
# Purpose:
#
# Author:      Christophe
#
# Created:     26/01/2014
# Copyright:   (c) Christophe 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import bluetooth

class BluetoothServer(object):
    """BluetoothServer"""

    def __init__(self):
        self.sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM ) # allocate socket

    def open(self,port):
        self.clients = []               # clear list of clients
        self.sock.bind(("",port))       # bind port to listen
        self.sock.listen(1)             # starts listenning (prm is backlog)

    def acceptConnection(self):
        csock,address = self.sock.accept()
        print "Accepted connection from ",address
        return csock

    def close(self):
        self.sock.close()


    def registerNewConnection(self,btc):
        # adds new bt connection to the list
        self.clients.append(btc)

    def removeClient(self,btc):
        self.clients.remove(btc)

    def closeClients(self):
        for i,btc in enumerate(self.clients):
            btc.close()
        del self.clients[:]