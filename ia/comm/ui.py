# -*- coding: utf-8 -*-

import logging
from comm.comm import Comm
from events.event import CmdError

class UI(Comm):
    u'''Comm robot-robot'''
    def __init__(self, socket):
        super(self.__class__, self).__init__(socket)
        self.logger = logging.getLogger(u"ui")
        
    def cmd_to_event(self, cmd):
        # si on utilise Comm.cmd_to_event, il faut prfixer toutes les 
        # commandes par "ui "
        if cmd == u"":
            self.logger.warning(u"No more data on socket.")
            return None
        words = cmd.lower().split()
        event = None
        try:
            m = __import__(u"events.ui")
            event = getattr(getattr(m,u"ui"), u"UIEvent")(words)
        except ImportError:
            raise CmdError(u"No module called  ui  found")
        return event

                    
        event = self.cmd_to_event(cmd)
        if event != None:
            self.event_manager.add_event(event)
