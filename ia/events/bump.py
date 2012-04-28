# -*- coding: utf-8 -*-

from events.event import Event
from events.event import CmdError

class BumpEvent(Event):
	def __init__(self, cmd):
		super(self.__class__,self).__init__()
		if len(cmd) == 3:
			self.pos = cmd[1]
			self.state = cmd[2]
		else:
			raise CmdError("« %s » takes exactly 2 arguments"%(cmd[0]))
