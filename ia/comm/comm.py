# -*- coding: ascii -*-

from threading import Thread, Event
from events.event import CmdError

import logging
import socket

class Comm(Thread):
    def __init__(self, socket):
        Thread.__init__(self)
        self.running    = Event( )
        self.logger     = logging.getLogger(u"comm")
        self.socket     = socket
        self.dispatcher = None
        
    def cmd_to_event(self, cmd):
        if cmd == u"":
            self.logger.warning(u"No more data on socket.")
            return None
        words = cmd.lower().split()
        if len(words) < 2:
            raise CmdError(u"All command require at least 2 arguments")
        w = words[0].capitalize()+u"Event"
        event = None
        
        try:
            m = __import__(u"events."+self.__class__.__name__.lower()+u"."+words[0]) #  tester
            event = getattr(getattr(getattr(m, self.__class__.__name__.lower()),words[0]), w)(words)
        except ImportError:
            raise CmdError(u"No module called  %s  found" %w)
        return event

                    
        event = self.cmd_to_event(cmd)
        if event != None:
            self.dispatcher.add_event(event)
    
    def run(self):
        if self.socket != None and self.dispatcher != None:
            self.bufsock   = self.socket.makefile(buffering=1,
                    errors=u'replace')
            while not self.running.isSet():
                try:
                    cmd = self.bufsock.readline()
                except socket.timeout, message:
                    self.logger.error(u"Receiver : timout. %s" % message)
                    #return None
                except socket.error, message:
                    self.logger(u"Receiver : socket error %s" % message)
                    break
                else:
                    try:
                        event = self.cmd_to_event(cmd)
                    except CmdError, e:
                        self.logger.error(u"Failed to parse  %s " %(cmd.strip()))
                        self.logger.error(u"\tMessage: %s" %e)
                    else:
                        if event == None:
                            self.logger.error(u"Event is None, breaking")
                            break
                        else:
                            self.dispatcher.add_event(event)
            

    def send(self, message):
        try:
            return self.socket.send(str(message+"\n").encode("ascii"))
        except socket.timeout, message:
            self.logger.error (u"Sender : timout %s" % message)
            return None
        except socket.error, message:
            self.logger.error (u"Sender : socket error %s" % message)
            return u"stop"
        
    def stop(self):
        self.running.set( )
        self.socket.shutdown(socket.SHUT_WR)
        self.socket.close()
