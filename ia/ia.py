#!/usr/bin/python3
# -*-coding:UTF-8 -*

import socket



#sock.setblocking(False)

#cmd = sock.makefile().readline()
#print("«"+cmd+"»")

#sock.send(b"rot -90\n")


from can import Can
from event_dispatcher import Event_dispatcher

class IA:
	def __init__(self, mission_prefix, ip, port=7773):
		assert(mission_prefix in ["petit", "grand"])
		self.mission_prefix = mission_prefix
		self.ip   = ip
		self.port = port
		self.sock = None
		self.connect()
		self.dispatcher = Event_dispatcher(self.mission_prefix)
		self.can  = Can(self.sock)
		
	def connect(self):
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.settimeout(0.5)
			self.sock.connect((self.ip, self.port))
		except socket.error as message:
			if self.socket: 
				self.socket.close()
			self.socket = None # On est sûr de tout arréter 
			# logger.fatal
			print ("Impossible d'otenir une connection : ", message)
			self.keep_on = False
		else:
			self.keep_on = True
			
		
		
	def main(self):

		while self.keep_on:
			# try:
			# pour les options : http://docs.python.org/py3k/library/functions.html#open
			
			event = self.can.receiver()
			if event == None:
				print("[main] Command not parsed")
			elif event == "stop": # utiliser éventuellement une exception
				break
			else:
				print(event)
				self.dispatcher.listener(event)
				

	def stop(self):
		self.sock.close()

#m.process_event("plop")
#m.actions[0]("plop")
#try:
#	print(m.actions[1])
#except KeyError:
#	pass

#print(state)


if __name__ == "__main__":
	ia = IA("petit", "r2d2")
	ia.main()