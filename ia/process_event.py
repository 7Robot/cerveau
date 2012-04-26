# -*- coding: utf-8 -*-

from events.event import CmdError
from events import *

def processEvent(cmd):
	words = cmd.lower().split()
	print("Split « %s » as "%cmd.strip(), words)
	if len(words) < 2:
		print("All command requiere at least 2 arguments")
		return None
	w = words[0].capitalize()+"Event"
	event = None
	try:
		m = __import__("events."+words[0])
		event = getattr(m, w)(words)
	except ImportError:
		print("No module called « %s » found" %w)
	except CmdError as e:
		print("Module « %s » failed to parse « %s »" %(w, cmd.strip()))
		print("\tMessage: %s" %e)
	return event
