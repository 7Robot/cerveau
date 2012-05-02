# -*- coding: utf-8 -*-

from threading import Thread
from events.event import CmdError
from events import *
import socket

class Can(Thread):
	def __init__(self, socket, event_manager):
		Thread.__init__(self)
		self.socket    = socket
		self.event_manager = event_manager
		self.bufsock   = self.socket.makefile(buffering=1,
                errors='replace')
		
	def cmd_to_event(self, cmd):
		if cmd == "":
			# EOF
			return "stop" # TODO exception
		words = cmd.lower().split()
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

					
		event = self.cmd_to_event(cmd)
		if event != None:
			self.event_manager.add_event(event)
	
	def run(self):
		while True:
			try:
				cmd = self.bufsock.readline()
			except socket.timeout as message:
				print ("Receiver : timout", message) #TODO: logger.fatal
				#return None
			except socket.error as message:
				print ("Receiver : socket error", message) #TODO: logger.fatal
				break
			else:
				event = self.cmd_to_event(cmd)
				if event=="stop":
					break
				self.event_manager.add_event(event)
			

	def sender(self, message):
		try:
			return self.socket.send(bytes(message+"\n", "utf-8"))
		except socket.timeout as message:
			print ("Sender : timout", message) #TODO: logger.fatal
			return None
		except socket.error as message:
			print ("Sender : socket error", message) #TODO: logger.fatal
			return "stop"
