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
            self.logger.debug("[old] %s" % message)
            if cmds[0] == "asserv":
                if len(cmds) == 3 and cmds[1] == "rot":
                    cmds[2] = str(-int(cmds[2]))
                elif len(cmds) >= 4 and cmds[1] == "speed":
                    left = cmds[2]
                    cmds[2] = cmds[3]
                    cmds[3] = left # old left = new right
            elif cmds[0] == "rangefinder":
                if len(cmds) > 1:
                    if cmds[1] == "1":
                        cmds[1] = "2"
                    elif cmds[1] == "2":
                        cmds[1] = "1"
            elif cmds[0] == "odo":
                if len(cmds) > 4:
                    cmds[2] = str(-int(cmds[2]))
                    cmds[4] = str((-int(cmds[4])+54000)%36000)
            elif cmds[0] == "ax":
                if len(cmds) >= 3 and cmds[2] == "angle" and cmds[3] == "set":
                    if cmds[1] == "2":
                        cmds[1] = "1"
                    elif cmds[1] == "1":
                        cmds[1] = "2"
            message = " ".join(cmds)
            self.logger.debug("[new] %s" % message)
        return self.queued_sender.add_action(message)
