# -*-coding:UTF-8 -*

from missions.mission import Mission
from robots.robot import Robot

class BottleMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)

    def start(self):
        if self.state == 0:
            self.create_timer(500)
            self.state += 1
            

    def process_event(self, e):
        if self.state == 1:
            if e.name == 'timer':
                self.state += 1
                self.missions["forward"].start(self, 2700)
                
        if self.state == 2:
            if e.name == "forward" and e.type == "done":
                self.state += 1
                if Robot.side == "violet":
                    self.missions["rotate"].start(self, -9200)
                else:
                    self.missions["rotate"].start(self, -8900)
                                    
        elif self.state == 3:
            if e.name == "rotate" and e.type == "done":
                self.state += 0.5
                self.create_timer(3000)
                #self.missions["speed"].start(80)
                self.missions["forward"].start(self, 13000) # TODO check avant totem 2
                
        elif self.state == 3.5:
            if e.name == "forward" and e.type == "done":
                self.state += 0.5
                for i in [1,2]: self.missions["threshold"].activate(i, False)
                self.missions["speed"].start(50)
                self.create_timer(10000)
                    
        elif self.state == 4:
            if (e.name == "bump" and e.state=="close") or e.name == "timer":
                self.state += 1
                self.missions["speed"].stop(self)
        
        elif self.state == 5:
            if e.name == "speed" and e.type == "done":
                self.state += 1        
                for i in [1,2]: self.missions["threshold"].activate(i, True)
                self.missions["forward"].start(self, -1300)
                
        elif self.state == 6:
            if e.name == "forward" and e.type == "done":
                self.state +=1
                if Robot.side == "violet":
                    self.missions["rotate"].start(self, 9000)
                else:
                    self.missions["rotate"].start(self, 9000)

        elif self.state == 7:
            if e.name == "rotate" and e.type == "done":
                self.state += 0.5
                # Avance de 142 cm
                #self.missions["double_chemin"].start(self, 14200, -4900, -9000)
                # J'ai mesuré 124cm avec un metre, tu aurais pas inversé le 2 et
                # le 4 ?
                self.missions["forward"].start(self, 14400)

        elif self.state == 7.5:
            if e.name == "forward" and e.type == "done":
                self.state += 0.5
                self.missions["forward"].start(self, -2000)
                
        elif self.state == 8:
            if e.name == "forward" and e.type == "done":
                self.state += 1
                self.missions["rotate"].start(self, -9000)
                    
        elif self.state == 9:
            if e.name == "rotate" and e.type == "done":
                self.state += 1
                for i in [1,2]: self.missions["threshold"].activate(i, False)
                self.missions["speed"].start(50)
                self.create_timer(10000)

                
        elif self.state == 10:
            if (e.name == "bump" and e.state=="close") or e.name == "timer":
                self.state += 1
                self.missions["speed"].stop(self)
                
        elif self.state == 11:
            if e.name == "speed" and e.type == "done":
                self.state += 1
                for i in [1,2]: self.missions["threshold"].activate(i, True)
     
