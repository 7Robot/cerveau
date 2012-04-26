# -*- coding: utf-8 -*-

from events.event import Event
from events.event import CmdError

class AsservEvent(Event):
	def __init__(self, cmd):
		self.type = cmd[1]
		if self.type == "dist" or self.type == "rot":
			if len(cmd) == 3:
				self.value = cmd[2]
			else:
				raise CmdError("« %s %s » takes exactly 1 argument"
						%(cmd[0], cmd[1]))
			try:
				self.value = int(self.value)
			except ValueError as e:
				raise CmdError(e.__str__())
		elif self.type == "speed":
			if len(cmd) == 4 or len(cmd) == 5:
				try:
					self.value = [int(cmd[2]), int(cmd[3])]
				except ValueError as e:
					raise CmdError(e.__str__())
				self.curt = False
				if len(cmd) == 5:
					if cmd[4] == "curt":
						self.curt = True
					else:
						raise CmdError("expected « curt » or nothing as fifth "
								+ "argument, got « %s »" %cmd[4])
			else:
				raise CmdError("« %s %s » takes exactly 2 or 3 arguments"
						%(cmd[0], cmd[1]))
		elif len(cmd) != 2:
			raise CmdError("« %s %s » takes no argument"
					 %(cmd[0], cmd[1]))

