# -*- coding: utf-8 -*-

from events.event import CmdError
from events import *
import socket

class Can:
	def __init__(self, socket):
		self.socket = socket

	def receiver(self):
		try:
			cmd = self.socket.makefile(buffering=1, errors='replace').readline()
		except socket.timeout as message:
			print ("Receiver : timout", message) #TODO: logger.fatal
			return None
		except socket.error as message:
			print ("Receiver : socket error", message) #TODO: logger.fatal
			return "stop"
		
		if cmd == "":
			# EOF
			return "stop"
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

	def sender(self, message):
		try:
			return self.socket.send(bytes(message+"\n", "utf-8"))
		except socket.timeout as message:
			print ("Sender : timout", message) #TODO: logger.fatal
			return None
		except socket.error as message:
			print ("Sender : socket error", message) #TODO: logger.fatal
			return "stop"