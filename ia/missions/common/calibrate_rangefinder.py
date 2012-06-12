# -*- coding: utf-8 -*-
u'''
Created on 11 mai 2012
'''

from __future__ import division
from missions.mission import Mission

class Calibrate_rangefinderMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = u"repos"
        self.nb_mesures = 16
        
    def process_event(self, event):
        if self.state == u"repos":
            if event.name == u"start":
                self.can.send(u"rangefinder %d unmute" % self.id)
                self.state        = u"calibrate rangefinder measurements"
                self.measurements = []
                self.logger.debug(u"Start calibration rangefinder %d" % self.id)
                    
        if self.state == u"calibrate rangefinder measurements":
            # on prend les 16 premires valeurs
            if event.name == u"rangefinder" and event.id == self.id \
                     and event.type == u"value":
                if len(self.measurements) < self.nb_mesures:
                    self.logger.debug(u"Calibrating rangefinder %d" % self.id)
                    self.measurements.append(event.value)
                else:
                    mean = sum(self.measurements)/len(self.measurements)
                    self.logger.debug(u"End calibration rangefinder %d" % self.id)
                    self.can.send(u"rangefinder %d mute" % event.id)
                    self.can.send(u"rangefinder %d mute" % event.id)
                    self.can.send(u"rangefinder %d threshold %d" % (self.id, mean))
                    self.ui.send(u"answer calibrate %d done, value is %d" % (self.id, mean))
                    self.state = u"repos"
                    
    def start(self, id):
        self.id = id
        super(self.__class__, self).start
