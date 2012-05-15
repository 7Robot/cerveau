# -*-coding:UTF-8 -*

from missions.mission import Mission
from robots.robot import Robot

class BottleNGMission(Mission):
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
                self.missions["forward"].start(self, 5800)
                
        if self.state == 2:
            if e.name == "forward" and e.type == "done":
                self.state += 1
                if Robot.side == "violet":
                    self.missions["rotate"].start(self, -9500)
                else:
                    self.missions["rotate"].start(self, -9050)
                                    
        elif self.state == 3:
            if e.name == "rotate" and e.type == "done":
                self.state += 1
                self.move.speed(40,40)
                    
        elif self.state == 4:
            if e.name == "bump" and e.state=="close":
                self.state += 1
                self.create_timer(500)
                
        elif self.state == 5:
            if e.name == "timer":
                self.state += 1
                self.move.stop(self)
        
        elif self.state == 6:
            if e.name == "speed" and e.type == "done":
                self.state += 1        
                self.missions["forward"].start(self, -1000)
                
        elif self.state == 7:
            if e.name == "forward" and e.type == "done":
                self.state +=1
                if Robot.side == "violet":
                    self.missions["rotate"].start(self, 9200)
                else:
                    self.missions["rotate"].start(self, 9400)

        elif self.state == 8:
            if e.name == "rotate" and e.type == "done":
                self.state += 1
                self.missions["forward"].start(self, 14200)
                
                
        
                
                
            
        
        elif self.state == 9:
            if e.name == "forward" and e.type == "done":
                self.state += 1
                self.missions["forward"].start(self, -2000)
                    
        elif self.state == 10:
            if e.name == "forward" and e.type == "done":
                self.state += 1
                self.missions["rotate"].start(self, -9000)
                
        elif self.state == 11:
            if e.name == "rotate" and e.type == "done":
                self.state += 1
                print('avance !!!!!!!!!!!!!!!!!!!')
                self.missions["speed"].start(20,20)
                print("fait !!!!")
                
        elif self.state == 12:
            if e.name == "bump" and e.state=="close":
                self.state += 1
                self.create_timer(500)
        
        elif self.state == 13:
            if e.name == "timer":
                self.state += 1
                self.move.stop(self)
                
        elif self.state == 14:
            if e.name == "speed" and e.type == "done":
                self.state += 1        
                self.missions["forward"].start(self, -2000)
                
        elif self.state == 15:
            if e.name == "forward" and e.type == "done":
                self.state += 1
                self.missions["rotate"].start(self, -9500)
                
      
