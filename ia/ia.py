#!/usr/bin/python3
# -*-coding:UTF-8 -*

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('r2d2', 7773))

#sock.setblocking(False)

#cmd = sock.makefile().readline()
#print("«"+cmd+"»")

#sock.send(b"rot -90\n")

from missions import *
from process_event import processEvent

m = MissionRecalage()

while True:
	cmd = sock.makefile().readline()
	event = processEvent(cmd)
	if event != None:
		print(event)
		print("[main] Send event to mission %s, state %d" %(m.name, m.state))
		m.processEvent(event)
	else:
		print("[main] Command not parsed")


#m.processEvent("plop")
#m.actions[0]("plop")
#try:
#	print(m.actions[1])
#except KeyError:
#	pass

#print(state)

sock.close()
