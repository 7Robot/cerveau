# -*- coding: utf-8 -*-

from events.event import Event
from events.event import CmdError

class SonarEvent(Event):
	def __init__(self, cmd):
		super(self.__class__,self).__init__()
		if len(cmd) == 3 or len(cmd) == 4:
			try:
				self.id = int(cmd[1])
			except ValueError as e:
				raise CmdError(e.__str__())
			self.pos = cmd[2]
			pos = [ "under", "over" ]
			if self.pos not in pos:
				raise CmdError("« %s » second argument must be in list "%cmd[0] + pos.__str__())
			self.edge = False
			if len(cmd) == 4:
				if cmd[3] == "edge":
					self.edge = True
				else:
					raise CmdError("expected « edge » or nothing as third "
							+ "argument, got « %s »"%cmd[3])
		else:
			raise CmdError("« %s » takes exactly 2 or 3 arguments"%(cmd[0]))
