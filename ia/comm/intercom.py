# -*- coding: utf-8 -*-
u'''
Created on 16 mai 2012
'''

# -*- coding: utf-8 -*-

from comm.comm import Comm
from comm.queued_sender import Queued_sender
from robots.robot import Robot

import logging


class InterCom(Comm):
    u'''Intercom'''
    def __init__(self, socket):
        super(self.__class__, self).__init__(socket)
        self.logger = logging.getLogger(u"intercom")
        self.queued_sender = Queued_sender(self.socket)
        self.queued_sender.start()
              
    
