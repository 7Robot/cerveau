# -*- coding: utf-8 -*-
u'''
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
            self.can.send(u"reset")
            self.create_timer(3000)

        # ODO SET
        elif self.state == 1:
            if event.name == u"timer":
                self.state += 1
                self.can.send(u"turret on")
                self.can.send(u"turret unmute")
                self.can.send(u"ax 1 torque set 800")
                self.can.send(u"ax 2 torque set 800")
                #self.odo.broadcast()
                self.odo.set(self, **{u"x": 0, u"y": 0, u"rot": 27000})

        # ODO SET OK
        elif self.state == 2:
            if event.name == u"odo" and event.type == u"done":
                self.state += 1
                self.ui.send(u"ia ready")

        # Demarrage de la mission positioning 1 sur bump back
        elif self.state == 3:
            print u"event: ", event
            if event.name == u"ui" and event.type == u"start":
                self.state += 1 
                self.missions[u"positioning1"].start()
            elif event.name == u"bump" and event.pos == u"back" and event.state == u"close":
                self.state += 1
                self.missions[u"positioning1"].start()

        # Fin de la premiere mission de positionnement
        elif self.state == 4:
            if event.name == u"positioning" and event.type == u"done":
                self.state += 1

        # Debut du match sur bump leash
        elif self.state == 5:
            if event.name == u"bump" and event.pos == u"leash" \
                    and event.state == u"open":
                self.state += 1
                # Set des threshold
                for i in [1, 2, 8]:
                    self.can.send(u"rangefinder %d threshold %d"
                            %(i, self.robot.rangefinder[i]))
                self.logger.info(u"Beggining of the match !")
                self.missions[u"match"].start()
                self.create_timer(3000)

        elif self.state == 6:
            if event.name == u"timer":
                self.state += 1
                self.missions[u"totem1"].start()

        #elif self.state == 6:
        #    if event.name == "totem" and event.type == "done":
        #        self.state += 1
        #        self.missions["positioning2"].start()

        elif self.state == 7:
            if event.name == u"totem" and event.type == u"done":
                self.state += 1
                self.missions[u"totem2"].start()

        elif self.state == 8:
            if event.name == u"totem" and event.type == u"done":
                self.can.send(u"reset")
            
            #self.missions["forward"].start(15000)
            #self.move.forward(self, 5000)
            #self.missions["rotate"].start(9000)
            #self.move.rotate(self, 9000)
            #self.missions["speed"].start(20, 20)
