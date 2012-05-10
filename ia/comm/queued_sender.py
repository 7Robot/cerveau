# -*- coding: utf-8 -*-

from queue import Queue
from threading import Thread, Event
import socket

class Queued_sender(Thread):
    '''envoie les actions sans saturer le medium de communication'''
    def __init__(self, socket):
        Thread.__init__(self)
        self.running= Event( )
        self.queue  = Queue()
        self.socket = socket
    
    def add_action(self, action):
        '''Inutile, sauf si on change d'implémentation'''
        action = bytes(action+"\n", "utf-8")
        self.queue.put(action, True, None) # block=True, timeout=None
        return len(action) # pour être compatible avec Comm.sender()
    
    def run(self):
        while not self.running.isSet( ):
            action = self.queue.get(True, None) # block=True, timeout=None
            try:
                self.socket.send(action)
            except socket.timeout as message:
                self.logger.error ("Sender : timout %s" % message)
            except socket.error as message:
                self.logger.error ("Sender : socket error %s" % message)
            self.running.wait(0.01) # 5ms entre chaque message
