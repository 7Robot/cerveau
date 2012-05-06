# -*- coding: utf-8 -*-

from events.event import Event
from events.event import CmdError

class RangefinderEvent(Event):
	def __init__(self, cmd):
		super(self.__class__,self).__init__()
		

		self.id  = self.parse_int(cmd[1])
		
		if len(cmd) >= 3:
			# rangefinder <id:int> mute
			# rangefinder <id:int> unmute
			self.type = cmd[2]
			
			types = ["mute", "unmute", "value", "threshold"]
			if self.type not in types:
				raise CmdError("« %s » third argument must be in list "%cmd[0] + types.__str__())
			
			# rangefinder <id:int> threshold <valeur:int>
			if self.type == "threshold":
				self.value = self.parse_int(cmd[3])
				
			# rangefinder <id:int> value <valeur:int> under|over [edge]
			elif self.type == "value":
				self.value = self.parse_int(cmd[3])
				self.pos   = cmd[4]
				self.edge  = False
				pos        = [ "under", "over" ]
				if len(cmd) == 6 and cmd[5] == "edge":
					self.edge = True
					
				if self.pos not in pos:
					raise CmdError("« %s » second argument must be in list "%cmd[0] + pos.__str__())
		

		else:
			raise CmdError("« %s » takes exactly 2 or more arguments"%(cmd[0]))
