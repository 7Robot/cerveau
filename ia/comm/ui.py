# -*- coding: utf-8 -*-

import logging
from comm.comm import Comm
from events.event import CmdError

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
