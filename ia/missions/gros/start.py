# -*- coding: utf-8 -*-
'''
Created on 27 avr. 2012
'''

from missions.mission import Mission
class StartMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)

    def process_event(self, event):
        # RESET, on attend 3 secondes
        if self.state == 0:
            self.state +=1
            self.can.send("reset")
            self.create_timer(3000)

        # ODO SET
        elif self.state == 1:
            if event.name == "timer":
                self.state += 1
                self.can.send("turret on")
                self.can.send("turret unmute")
                self.can.send("ax 1 torque set 800")
                self.can.send("ax 2 torque set 800")
                #self.odo.broadcast()
                self.odo.set(self, **{"x": 0, "y": 0, "rot": 27000})

        # ODO SET OK
        elif self.state == 2:
            if event.name == "odo" and event.type == "done":
                self.state += 1
                self.ui.send("ia ready")

        # Demarrage de la mission positioning 1 sur bump back
        elif self.state == 3:
            print("event: ", event)
            if event.name == "ui" and event.type == "start":
                self.state += 1 
                self.missions["positioning1"].start()
            elif event.name == "bump" and event.pos == "back" and event.state == "close":
                self.state += 1
                self.missions["positioning1"].start()

        # Fin de la premiere mission de positionnement
        elif self.state == 4:
            if event.name == "positioning" and event.type == "done":
                self.state += 1

        # Debut du match sur bump leash
        elif self.state == 5:
            if event.name == "bump" and event.pos == "leash" \
                    and event.state == "open":
                self.state += 1
                # Set des threshold
                for i in [1, 2, 8]:
                    self.can.send("rangefinder %d threshold %d"
                            %(i, self.robot.rangefinder[i]))
                self.logger.info("Beggining of the match !")
                self.missions["match"].start()
                self.create_timer(3000)

        elif self.state == 6:
            if event.name == "timer":
                self.state += 1
                self.missions["totem1"].start()

        #elif self.state == 6:
        #    if event.name == "totem" and event.type == "done":
        #        self.state += 1
        #        self.missions["positioning2"].start()

        elif self.state == 7:
            if event.name == "totem" and event.type == "done":
                self.state += 1
                self.missions["totem2"].start()
            
            #self.missions["forward"].start(15000)
            #self.move.forward(self, 5000)
            #self.missions["rotate"].start(9000)
            #self.move.rotate(self, 9000)
            #self.missions["speed"].start(20, 20)
