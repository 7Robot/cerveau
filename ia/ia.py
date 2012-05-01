#!/usr/bin/python3
# -*-coding:UTF-8 -*

import socket

from can import Can
from robot.small_robot import Small_robot
from event_dispatcher import Event_dispatcher

class IA:
	def __init__(self, robot, ip="localhost", port=7773):
		self.mission_prefix = robot.__class__.__name__.lower().split('_')[0]
		print("Starting « %s » robot" % self.mission_prefix)
		# On ne peut pas avoir "simu" car la class proxy renvoie le __class__.__name__ de l'objet proxié
		assert(self.mission_prefix in ["small", "big", "simu"])
		self.ip   = ip
		self.port = port
		self.sock = None
		self.connect()
		self.can  = Can(self.sock)
		self.robot = robot
		self.robot.can = self.can
		self.dispatcher = Event_dispatcher(self.mission_prefix, self.robot)
		
		
	def connect(self):
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect((self.ip, self.port))
		except socket.error as message:
			if self.sock:
				self.sock.shutdown(socket.SHUT_WR) 
				self.sock.close()
			self.sock = None # On est sûr de tout arréter 
			# logger.fatal
			print (self.ip, self.port)
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
	ia = IA(Small_robot())
	ia.main()
