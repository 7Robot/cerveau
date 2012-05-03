# -*- coding: utf-8 -*-

from threading import Thread
from events.event import CmdError
from events import *
import socket


class Can(Thread):
    def __init__(self, socket, event_manager):
        Thread.__init__(self)
        self.socket    = socket
        self.event_manager = event_manager
        
    def cmd_to_event(self, cmd):
        if cmd == "":
            # EOF
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
        self.bufsock   = self.socket.makefile(buffering=1,
                errors='replace')
        while True:
            try:
                cmd = self.bufsock.readline()
            except socket.timeout as message:
                print ("Receiver : timout", message) #TODO: logger.fatal
                #return None
            except socket.error as message:
                print ("Receiver : socket error", message) #TODO: logger.fatal
                break
            else:
                try:
                    event = self.cmd_to_event(cmd)
                except CmdError as e:
                    print("Failed to parse « %s »" %(cmd.strip()))
                    print("\tMessage: %s" %e)
                else:
                    if event == None:
                        break
                    else:
                        self.event_manager.add_event(event)
            

    def sender(self, message):
        try:
            return self.socket.send(bytes(message+"\n", "utf-8"))
        except socket.timeout as message:
            print ("Sender : timout", message) #TODO: logger.fatal
            return None
        except socket.error as message:
            print ("Sender : socket error", message) #TODO: logger.fatal
            return "stop"
