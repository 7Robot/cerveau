# -*- coding: utf-8 -*-

from threading import Thread
from events.event import CmdError
from events import *

import logging
from queue import Queue
import socket
import threading

class Comm(Thread):
    def __init__(self, socket, event_manager):
        Thread.__init__(self)
        self.logger = logging.getLogger("comm")
        self.socket    = socket
        self.event_manager = event_manager
        
    def cmd_to_event(self, cmd):
        if cmd == "":
            self.logger.warning("No more data on socket.")
            return None
        words = cmd.lower().split()
        if len(words) < 2:
            raise CmdError("All command require at least 2 arguments")
        w = words[0].capitalize()+"Event"
        event = None
        try:
            m = __import__("events."+words[0])
            event = getattr(m, w)(words)
        except ImportError:
            raise CmdError("No module called « %s » found" %w)
        return event

                    
        event = self.cmd_to_event(cmd)
        if event != None:
            self.event_manager.add_event(event)
    
    def run(self):
        if self.socket != None:
            self.bufsock   = self.socket.makefile(buffering=1,
                    errors='replace')
            while True:
                try:
                    cmd = self.bufsock.readline()
                except socket.timeout as message:
                    self.logger.error("Receiver : timout. %s" % message)
                    #return None
                except socket.error as message:
                    self.logger("Receiver : socket error %s" % message)
                    break
                else:
                    try:
                        event = self.cmd_to_event(cmd)
                    except CmdError as e:
                        self.logger.error("Failed to parse « %s »" %(cmd.strip()))
                        self.logger.error("\tMessage: %s" %e)
                    else:
                        if event == None:
                            self.logger.error("Event is None, breaking")
                            break
                        else:
                            self.event_manager.add_event(event)
            

    def sender(self, message):
        try:
            return self.socket.send(bytes(message+"\n", "utf-8"))
        except socket.timeout as message:
            self.logger.error ("Sender : timout %s" % message)
            return None
        except socket.error as message:
            self.logger.error ("Sender : socket error %s" % message)
            return "stop"

class Can(Comm):
    '''Comm sur le bus can'''
    def __init__(self, socket, event_manager):
        super(self.__class__, self).__init__(socket, event_manager)
        self.logger = logging.getLogger("can")
        self.queued_sender = Queued_sender(self.socket)
        self.queued_sender.start()
        
    def sender(self, message):
        return self.queued_sender.add_action(message)
        
class Wifi(Comm):
    '''Comm robot-robot'''
    def __init__(self, socket, event_manager):
        super(self.__class__, self).__init__(socket, event_manager)
        self.logger = logging.getLogger("wifi")
        
class UI(Comm):
    '''Comm robot-robot'''
    def __init__(self, socket, event_manager):
        super(self.__class__, self).__init__(socket, event_manager)
        self.logger = logging.getLogger("ui")
        
    def cmd_to_event(self, cmd):
        # si on utilise Comm.cmd_to_event, il faut préfixer toutes les 
        # commandes par "ui "
        if cmd == "":
            self.logger.warning("No more data on socket.")
            return None
        words = cmd.lower().split()
        if len(words) < 2:
            raise CmdError("All command require at least 2 arguments")
        event = None
        try:
            m = __import__("events.ui")
            event = getattr(m, "UIEvent")(words)
        except ImportError:
            raise CmdError("No module called « ui » found")
        return event

                    
        event = self.cmd_to_event(cmd)
        if event != None:
            self.event_manager.add_event(event)
            
            

class Queued_sender(Thread): # FIXME renommer en Event_Manager
    '''envoie les actions sans saturer le medium de communication'''
    def __init__(self, socket):
        Thread.__init__(self)
        self.running= threading.Event( )
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
