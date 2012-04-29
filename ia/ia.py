#!/usr/bin/python3
# -*-coding:UTF-8 -*

import socket

from can import Can
from robot import Robot
from event_dispatcher import Event_dispatcher

class IA:
	def __init__(self, mission_prefix, ip="r2d2", port=7773):
		assert(mission_prefix in ["petit", "grand", "tests"])
		self.mission_prefix = mission_prefix
		self.ip   = ip
		self.port = port
		self.sock = None
		self.connect()
		self.can  = Can(self.sock)
		self.robot = Robot(3000, 3000, 0, None, None, None, None, self.can)
		self.dispatcher = Event_dispatcher(self.mission_prefix, self.robot)
		
		
	def connect(self):
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect((self.ip, self.port))
		except socket.error as message:
			if self.socket:
				self.socket.shutdown(socket.SHUT_WR) 
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
				self.stop()
				break
			else:
				print(event)
				self.dispatcher.listener(event)
				

	def stop(self):
		self.sock.shutdown(socket.SHUT_WR) 
		self.sock.close()

if __name__ == "__main__":
	ia = IA("tests", "r2d2")
	ia.main()
