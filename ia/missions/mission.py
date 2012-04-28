# -*-coding:UTF-8 -*

import threading
from events.internal import Timer_end

class Mission:
	def __init__(self, name):
		''' Convention state = 0 : état initial (d'attente)
		'''
		self.state = 0
		self.name = name
	def process_event(self, event):
		pass
	def create_timer(self, duration):
		'''Créé un timer qui va envoyer un évènement
		duration'''
		t = threading.Timer(duration/1000, self.process_event, [Timer_end()])
		t.start()