# -*- coding: utf-8 -*-

from comm.comm import Comm
from comm.queued_sender import Queued_sender
from robots.robot import Robot

import logging


class Can(Comm):
    '''Comm sur le bus can'''
    def __init__(self, socket):
        super(self.__class__, self).__init__(socket)
        self.logger = logging.getLogger("can")
        self.queued_sender = Queued_sender(self.socket)
        self.queued_sender.start()
              
    def send(self, message):
        if Robot.side == "red":
            cmds = message.lower().split()
            if cmds[0] == "asserv":
                if len(cmds) == 3 and cmds[1] == "rot":
                    cmds[2] = str(-int(cmds[2]))
                elif len(cmds) >= 4 and cmds[1] == "speed":
                    left = cmds[2]
                    cmds[2] = cmds[3]
                    cmds[3] = left # old left = new right
                message = " ".join(cmds)
        return self.queued_sender.add_action(message)
