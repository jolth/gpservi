# -*- coding: UTF-8 -*-
"""
    Daemons for GPS

    Autor: Jorge A. Toro [jolthgs@gmail.com]

    Usage:
    >>> import daemon
    >>> d = daemon.DaemonUDP('', 50007, 256)
    >>> d.start()
    Server run :50007
    >>> d.run()

    >>> d1 = daemon.DaemonTCP('127.0.0.1', 50009, 256)
    >>> d1.start()
    >>> d1.run()

"""
import sys
import socket
import threading
from Log.logFile import createLogFile, logFile
from Load.loadconfig import load
import Devices.devices    

class DaemonUDP:
    """
        Server UDP
    """
    endfile = 0
    lock = threading.Lock()

    def __init__(self, host, port, buffering):

        self.host = host
        self.port = port
        self.buffering = buffering
        self.server = None 
        self.running = 1 
        self.thread = None 


    def start(self):
        """
            Prepara el servidor 
        """

        if createLogFile(str(load('FILELOG', 'FILE'))): 
            try:
                self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
                self.server.bind((self.host, self.port))
                print >> sys.stdout, ("Server run %s:%s" % (self.host, self.port))
            except socket.error, (value, message):
                if self.server:
                    self.server.close()
                print >> sys.stderr, "Could not open socket:", message
                sys.exit(1)

        
    def run(self):
        """ 
            threading 
        """
        while self.running:
            try:
                data, address = self.server.recvfrom(self.buffering) 
                self.thread = threading.Thread(target=self.threads, args=(data, address, self.__class__.lock, ))
                self.thread.start()
            except KeyboardInterrupt: 
                sys.stderr.write("\rExit, KeyboardInterrupt\n")
                try:
                    sys.stdout.write("Exit App... \n")
                    self.server.close()
                    self.thread.join() 
                                       
                    raise SystemExit("Se terminaron de ejecutar todos los dispositivos activos en el servidor")
                except AttributeError, NameError: pass

                break 



    def threads(self, data, address, lock):
        """
            run thread
        """
        # Parse Devices
        rawData = Devices.devices.getTypeClass(data, address) 
        
        if not rawData.has_key('id'): 
            print >> sys.stdout, rawData
            return 

        ### Eventos
        import Event.captureEvent
        event = Event.captureEvent.parseEvent(rawData) 
                                                       
        ### Escribe el la Tabla de Log
        import Log.logDB as LogDB
        LogDB.insertLog(rawData)
        # End Tabla de Log

        #### Escribe en el Fichero de Log
        lock.acquire(True)
        self.__class__.endfile = logFile(str(load('FILELOG', 'FILE')),
                                         self.__class__.endfile,
                                         raw=rawData 
                                        )
        lock.release()
        # End Fichero de Log




class DaemonTCP:
    """
        Server TCP

    """
    def __init__(self, host, port, buffering):
        self.host = host
        self.port = port
        self.buffering = buffering
        self.server = None

    def start(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            self.server.bind((self.host,self.port)) 
            self.server.listen(5) 
            print ("Server run %s:%s" % (self.host, self.port))
        except socket.error, (value, message):
            if self.server:
                self.server.close()
            print "Could not open socket:", message 
            sys.exit(1)

        
    def run(self):
        pass
