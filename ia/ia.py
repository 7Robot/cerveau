#!/usr/bin/python3
# -*-coding:UTF-8 -*

import socket



#sock.setblocking(False)

#cmd = sock.makefile().readline()
#print("«"+cmd+"»")

#sock.send(b"rot -90\n")


from process_event import processEvent
from event_dispatcher import Event_dispatcher

class IA:
	def __init__(self, mission_prefix, ip):
		assert(mission_prefix in ["petit", "grand"])
		self.mission_prefix = mission_prefix
		self.ip = ip
		self.connect()
		
	def connect(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((self.ip, 7773))
		self.dispatcher = Event_dispatcher(self.mission_prefix)
		
	def main(self):

		while True:
			# try:
			cmd = self.sock.makefile().readline()
			event = processEvent(cmd)
			if event != None:
				print(event)
				self.dispatcher.listener(event)
			else:
				print("[main] Command not parsed")

	def stop(self):
		self.sock.close()

#m.processEvent("plop")
#m.actions[0]("plop")
#try:
#	print(m.actions[1])
#except KeyError:
#	pass

#print(state)


if __name__ == "__main__":
	ia = IA("petit", "r2d2")
	ia.main()