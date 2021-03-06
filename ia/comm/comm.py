# -*- coding: ascii -*-

from threading import Thread, Event
from events.event import CmdError

import logging
import socket

class Comm(Thread):
    def __init__(self, socket):
        Thread.__init__(self)
        self.running    = Event( )
        self.logger     = logging.getLogger("comm")
        self.socket     = socket
        self.dispatcher = None
        
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
            m = __import__("events."+self.__class__.__name__.lower()+"."+words[0]) #  tester
            event = getattr(getattr(getattr(m, self.__class__.__name__.lower()),words[0]), w)(words)
        except ImportError:
            raise CmdError("No module called  %s  found" %w)
        return event

                    
        event = self.cmd_to_event(cmd)
        if event != None:
            self.dispatcher.add_event(event)
    
    def run(self):
        if self.socket != None and self.dispatcher != None:
            self.bufsock   = self.socket.makefile(buffering=1,
                    errors='replace')
            while not self.running.isSet():
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
                        self.logger.error("Failed to parse  %s " %(cmd.strip()))
                        self.logger.error("\tMessage: %s" %e)
                    else:
                        if event == None:
                            self.logger.error("Event is None, breaking")
                            break
                        else:
                            self.dispatcher.add_event(event)
            

    def send(self, message):
        try:
            return self.socket.send(bytes(message+"\n", "ascii"))
        except socket.timeout as message:
            self.logger.error ("Sender : timout %s" % message)
            return None
        except socket.error as message:
            self.logger.error ("Sender : socket error %s" % message)
            return "stop"
        
    def stop(self):
        self.running.set( )
        self.socket.shutdown(socket.SHUT_WR)
        self.socket.close()
