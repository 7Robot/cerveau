# -*-coding:UTF-8 -*

from missions.mission import Mission

class BottleOldMission(Mission):
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
                self.can.send("asserv dist 2600")
                
        if self.state == 2:
            if e.name == "asserv" and e.type == "done":
                self.state += 1
                self.can.send("asserv rot -9500")
                                    
        elif self.state == 3:
            if e.name == "asserv" and e.type == "done":
                self.state += 1
                self.can.send("asserv speed 40 40")
                    
        elif self.state == 4:
            if e.name == "bump" and e.state=="close":
                self.state += 1
                self.create_timer(500)
                
        elif self.state == 5:
            if e.name == "timer":
                self.state += 1
                self.can.send("asserv stop")
        
        elif self.state == 6:
            if e.name == "asserv" and e.type == "done":
                self.state += 1        
                self.can.send("asserv dist -1000")
                
        elif self.state == 7:
            if e.name == "asserv" and e.type == "done":
                self.state +=1
                self.can.send("asserv rot 9200")

        elif self.state == 8:
            if e.name == "asserv" and e.type == "done":
                self.state += 1
                self.can.send("asserv dist 14200")
        
        elif self.state == 9:
            if e.name == "asserv" and e.type == "done":
                self.state += 1
                self.can.send("asserv dist -2000")
                    
        elif self.state == 10:
            if e.name == "asserv" and e.type == "done":
                self.state += 1
                self.can.send("asserv rot -9000")
                
        elif self.state == 11:
            if e.name == "asserv" and e.type == "done":
                self.state += 1
                self.can.send("asserv speed 20 20")
                
        elif self.state == 12:
            if e.name == "bump" and e.state=="close":
                self.state += 1
                self.create_timer(500)
        
        elif self.state == 13:
            if e.name == "timer":
                self.state += 1
                self.can.send("asserv stop")
                
        elif self.state == 14:
            if e.name == "asserv" and e.type == "done":
                self.state += 1        
                self.can.send("asserv dist -2000")
                
        elif self.state == 15:
            if e.name == "asserv" and e.type == "done":
                self.state += 1
                self.can.send("asserv rot -9500")
                
        