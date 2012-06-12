# -*- coding: utf-8 -*-
u'''
Created on 6 mai 2012
'''
from events.event import Event
from missions.mission import Mission
from robots.robot import Robot

class UIMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = u"repos"
        
    def process_event(self, event):
        if self.state == u"repos":
            if event.name == u"ui":
                if event.type == u"calibrate":
                    if u"calibrate_rangefinder" in self.missions:
                        self.missions[u"calibrate_rangefinder"].start(event.id)
                    else:
                        self.logger.error(u"The mission \'calibrate_rangefinder\' is not loaded")
                    
                elif event.type == u"get":
                    if event.mission in self.missions:
                        ans = getattr(self.missions[event.mission], event.attribute)
                        self.ui.send(u"answer %s" % (ans.__str__()))
                    else:
                        self.ui.send(u"exception mission %s not found" % (event.mission))
                        
                elif event.type == u"end":
                    print u"Stopping the ia"
                    self.ui.send(u"stopping")
                    self.ui.stop()
                    self.can.stop()
                    #self.inter.stop()
                    # TODO: killer les autres threads
                        
                elif event.type == u"init":
                    Robot.side = event.side
                    self.ui.send(u"answer done")
                    self.send_event(Event(u"ui", u"start", self.missions[u"start"]))
                
                elif event.type == u"message":
                    self.logger.info(u"UI says: %s" % event.message) 
                        
                        
                elif event.type == u"positioning":
                    if u"positioning1" in self.missions:
                        self.missions[u"positioning1"].start()
                    else:
                        self.logger.error(u"The mission \'positioning\' is not loaded")
                        
                elif event.type == u"set":
                    if event.mission in self.missions:
                        value = event.value 
                        # TODO: double check selon le type de l'attribut
                        try:
                            setattr(self.missions[event.mission], event.attribute, value)
                        except AttributeError, e:
                            self.ui.send(u"exception %s" % e)
                        else:
                            self.ui.send(u"answer done")
                    else:
                        self.ui.send(u"exception mission %s not found" % (event.mission))
                        
                        
                elif event.type == u"test":
                    if event.test == u"forward":
                        self.missions[u"forward"].start(self, 1000)
                        self.ui.send(u"answer done")
                        
                        
      
