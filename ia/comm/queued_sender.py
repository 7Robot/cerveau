# -*- coding: ascii -*-

import logging
from Queue import Queue
from threading import Thread, Event
import socket

class Queued_sender(Thread):
    u'''envoie les actions sans saturer le medium de communication'''
    def __init__(self, socket):
        Thread.__init__(self)
        self.running= Event( )
        self.Queue  = Queue()
        self.socket = socket
        self.logger = logging.getLogger(u"queued_sender")
    
    def add_action(self, action):
        u'''Inutile, sauf si on change d'implmentation'''
        action =str(action+"\n").encode("ascii")
        self.Queue.put(action, True, None) # block=True, timeout=None
        return len(action) # pour tre compatible avec Comm.sender()
    
    def run(self):
        while not self.running.isSet( ):
            action = self.Queue.get(True, None) # block=True, timeout=None
            try:
                self.socket.send(action)
            except socket.timeout, message:
                self.logger.error (u"Sender : timout %s" % message)
            except socket.error, message:
                self.logger.error (u"Sender : socket error %s" % message)
            self.running.wait(0.01) # 50ms entre chaque message
