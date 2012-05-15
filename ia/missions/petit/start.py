# -*- coding: ascii -*-
'''
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
            self.can.send("reset")
            self.create_timer(3000) # FIXME 30000 !!!!!!!!!!!!!!!
            

        elif self.state == 1:
            if event.name == "timer":
                self.state += 1
                self.can.send("turret on")
                self.can.send("turret unmute")
                for i in [1, 2, 8]:
                    self.can.send("rangefinder %d threshold %d"
                            % (i, Robot.rangefinder[i]))
                self.ui.send("ia ready")
#                self.missions["positioning"].start()
#                self.missions["bottle"].start()
#                self.missions["double_chemin"].start(self, 14200)
#                self.missions["calibraterotation"].start()
#                self.can.send("asserv dist 3000") # Fake recalibration
#                self.odo.broadcast()
#                self.can.send("turret unmute")
#                self.odo.set(self, **{"x": 0, "y": 0, "rot": 90})
#
        elif self.state == 2:
            if event.name == "positioning" and event.type == "done":
                self.state += 1
                
                
#                self.missions["forward"].start(self, 9000)
                print("Gooooooooooooooooo")
#            if event.name == "odo" and event.type == "done":
#                self.state += 1
#
        elif self.state == 3:
            if event.name == "bump" and event.state == "open" \
                    and event.pos == "leash":
                self.state += 1
                self.missions["match"].start()
                self.missions["bottle"].start()
                
                
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
