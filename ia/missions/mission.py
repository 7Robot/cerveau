# -*-coding:UTF-8 -*

import threading
from events.internal import Timer_end

class Mission:
	def __init__(self, name):
		''' Convention state = 0 : état initial (d'attente)
		'''
		self.state = 0
		self.name = name
	def processEvent(self, event):
		pass
	def createTimer(self, duration):
		'''Créé un timer qui va envoyer un évènement
		duration'''
		t = threading.Timer(duration/1000, self.processEvent, [Timer_end()])
		t.start()