# -*- coding: utf-8 -*-

from comm.comm import Comm
from comm.queued_sender import Queued_sender

import logging


class Can(Comm):
    '''Comm sur le bus can'''
    def __init__(self, socket, event_manager):
        super(self.__class__, self).__init__(socket, event_manager)
        self.logger = logging.getLogger("can")
        self.queued_sender = Queued_sender(self.socket)
        self.queued_sender.start()
              
    def sender(self, message):
        return self.queued_sender.add_action(message)
