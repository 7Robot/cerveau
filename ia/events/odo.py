# -*- coding: utf-8 -*-

from events.event import Event
from events.event import CmdError

class OdoEvent(Event):
	def __init__(self, cmd):
		self.type = cmd[1]
		if self.type == "pos" or self.type == "set":
			if len(cmd) == 5:
				try:
					self.value = list(map(int,cmd[2:]))
				except ValueError as e:
					raise CmdError(e.__str__())
			else:
				raise CmdError("« %s %s » takes exactly 3 arguments (x, y, theta)"
						%(cmd[0], cmd[1]))
		elif len(cmd) != 2:
			raise CmdError("« %s %s » takes no argument"
			 	%(cmd[0], cmd[1]))
