# -*- coding: ascii -*-
u'''
Created on 27 avr. 2012
'''

from missions.mission import Mission
from robots.robot import Robot 

class StartMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)

    def process_event(self, event):
        if self.state == 0:
            self.state +=1
            self.can.send(u"reset")
            self.create_timer(3000)

        elif self.state == 1:
            if event.name == u"timer":
                self.state += 0.5
                self.can.send(u"turret on")
                self.can.send(u"turret unmute")
                self.ui.send(u"ia ready")
                
#                self.missions["positioning"].start()
#                self.missions["bottle"].start()
#                self.missions["double_chemin"].start(self, 14200, -4900, -9000)
#                self.missions["calibraterotation"].start()
#                self.can.send("asserv dist 3000") # Fake recalibration
#                self.odo.broadcast()
#                self.can.send("turret unmute")
#                self.odo.set(self, **{"x": 0, "y": 0, "rot": 90})
#
        elif self.state == 1.5:
            if event.name == u"ui" and event.type == u"start":
                self.state += 0.5
                self.missions[u"positioning"].start()

        elif self.state == 2:
            if event.name == u"positioning" and event.type == u"done":
                for i in [1, 2, 8]:
                    self.can.send(u"rangefinder %d threshold %d"
                            % (i, Robot.rangefinder[i]))
                self.state += 1
                
        elif self.state == 3:
            if event.name == u"bump" and event.state == u"open" \
                    and event.pos == u"leash":
                self.state += 1
                self.logger.info(u"Beggining of the match !")
                self.missions[u"match"].start()
                self.missions[u"bottle"].start()
                
                
##                self.missions["positioning"].start()
#                print("GO !!!!!!!!!!")
##                self.missions["test"].start()
#                
#
#        elif self.state == 4:
#            if event.name == "move" and event.type == "done":
#                self.state += 1
#
#        elif self.state == 5:
#            if event.name == "bump" and event.pos == "leash" \
#                    and event.state == "open":
#                self.can.send("turret on")
#                for i in [1, 2, 8]:
#                    self.can.send("rangefinder %d threshold %d"
#                            % (i, self.robot.rangefinder[i]))
#                self.logger.info("Beggining of the match !")
#                # On indique  l'UI que le match a commenc
#                self.ui.send("start")
#                self.missions["end_match"].start()
#                self.missions["forward"].start(15000)

            
            #self.missions["forward"].start(15000)
            #self.move.forward(self, 5000)
            #self.missions["rotate"].start(9000)
            #self.move.rotate(self, 9000)
            #self.missions["speed"].start(20, 20)
