# -*- coding: utf-8 -*-

from events.event import Event
from events.event import CmdError
from mathutils.types import Vertex
from robots.robot import Robot

class OdoEvent(Event):
  def __init__(self, cmd):
    super(self.__class__,self).__init__()
    self.type  = cmd[1]
    if self.type == "pos" or self.type == "set":
      if len(cmd) == 5:
        try:
          l = list(map(int,cmd[2:]))
          self.pos = Vertex(l[0] * 10, l[1] * 10)
          self.rot   = l[2]
          if Robot.side == "red":
            '''On inverse pas les x car quand on dmarre de rouge
            on fait croire  l'ia et l'odo que notre orientation 
            initiale est 0'''
            self.pos.x = -self.pos.x
            self.rot   = (-self.rot + 54000) % 36000 
        except ValueError as e:
          raise CmdError(e.__str__())
      else:
        raise CmdError(" %s %s  takes exactly 3 arguments (x, y, theta)"
            %(cmd[0], cmd[1]))
    elif len(cmd) != 2:
      raise CmdError(" %s %s  takes no argument"
         %(cmd[0], cmd[1]))
