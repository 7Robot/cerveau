# -*- coding: utf-8 -*-
'''
Created on 11 mai 2012
'''

from missions.mission import Mission


class Calibrate_rangefinderMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = "repos"
        self.nb_mesures = 16
        
    def process_event(self, event):
        if self.state == "repos":
            if event.name == "start":
                self.can.send("rangefinder %d unmute" % self.id)
                self.state        = "calibrate rangefinder measurements"
                self.measurements = []
                self.logger.debug("Start calibration rangefinder %d" % self.id)
                    
        if self.state == "calibrate rangefinder measurements":
            # on prend les 16 premires valeurs
            if event.name == "rangefinder" and event.id == self.id \
                     and event.type == "value":
                if len(self.measurements) < self.nb_mesures:
                    self.logger.debug("Calibrating rangefinder %d" % self.id)
                    self.measurements.append(event.value)
                else:
                    mean = sum(self.measurements)/len(self.measurements)
                    self.logger.debug("End calibration rangefinder %d" % self.id)
                    self.can.send("rangefinder %d mute" % event.id)
                    self.can.send("rangefinder %d mute" % event.id)
                    self.can.send("rangefinder %d threshold %d" % (self.id, mean))
                    self.ui.send("answer calibrate %d done, value is %d" % (self.id, mean))
                    self.state = "repos"
                    
    def start(self, id):
        self.id = id
        super(self.__class__, self).start
