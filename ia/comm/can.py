# -*- coding: utf-8 -*-

from comm.comm import Comm
from comm.queued_sender import Queued_sender
from robots.robot import Robot

import logging


class Can(Comm):
    u'''Comm sur le bus can'''
    def __init__(self, socket):
        super(self.__class__, self).__init__(socket)
        self.logger = logging.getLogger(u"can")
        self.queued_sender = Queued_sender(self.socket)
        self.queued_sender.start()
              
    def send(self, message):
        if Robot.side == u"red":
            cmds = message.lower().split()
            self.logger.debug(u"[old] %s" % message)
            if cmds[0] == u"asserv":
                if len(cmds) == 3 and cmds[1] == u"rot":
                    cmds[2] = unicode(-int(cmds[2]))
                elif len(cmds) >= 4 and cmds[1] == u"speed":
                    left = cmds[2]
                    cmds[2] = cmds[3]
                    cmds[3] = left # old left = new right
            elif cmds[0] == u"rangefinder":
                if len(cmds) > 1:
                    if cmds[1] == u"1":
                        cmds[1] = u"2"
                    elif cmds[1] == u"2":
                        cmds[1] = u"1"
            elif cmds[0] == u"odo":
                if len(cmds) > 4:
                    cmds[2] = unicode(-int(cmds[2]))
                    cmds[4] = unicode((-int(cmds[4])+54000)%36000)
            elif cmds[0] == u"ax":
                if len(cmds) >= 3 and cmds[2] == u"angle" and cmds[3] == u"set":
                    if cmds[1] == u"2":
                        cmds[1] = u"1"
                    elif cmds[1] == u"1":
                        cmds[1] = u"2"
            message = u" ".join(cmds)
            self.logger.debug(u"[new] %s" % message)
        return self.queued_sender.add_action(message)
