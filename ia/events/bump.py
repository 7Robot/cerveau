# -*- coding: utf-8 -*-

from events.event import Event
from events.event import CmdError

class BumpEvent(Event):
	def __init__(self, cmd):
		if len(cmd) == 3:
			self.pos = cmd[1]
			try:
				self.state = int(cmd[2])
			except ValueError as e:
				raise CmdError(e.__str__())
			if self.state in  [ 0, 1 ]:
				self.state = bool(self.state)
			else:
				raise CmdError("« %s » second argument must be 0 or 1"%cmd[0])
		else:
			raise CmdError("« %s » takes exactly 2 arguments"%(cmd[0]))
