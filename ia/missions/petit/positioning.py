# -*-coding:UTF-8 -*

from missions.mission import Mission

class PositioningMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)

    def start(self):
        if self.state == 0:
            self.move.rotate(9000)
            self.state += 1

    def process_event(self, e):
        if self.state == 1:
            if e.name == "asserv" and e.type == "done":
                self.move.speed(-20, -20)
                self.state += 1
                                    
        elif self.state == 2:
            if e.name == "bump" and e.state == "close":
                self.create_timer(700)
                self.state += 1
                    
        elif self.state == 3:
            if e.name == "timer":
                # self.robot.set_y(self.robot.dim_b - 10000)
                self.move.stop()
                self.robot.forward(1500)
                self.state += 1
                    
        elif self.state == 4:
            if e.name == "asserv" and e.type == "done":
                self.robot.rotate(-9000)
                self.state += 1
                self.logger.info("Positioning (5) : asserv done")
                    
        elif self.state == 5:
            if e.name == "asserv" and e.type == "done":
                self.robot.asserv(-20, -20)
                self.state += 1

        elif self.state == 6:
            if e.name == "bump" and e.state == "close":
                self.robot.set_x(self.robot.dim_b - 15000)
                self.robot.theta = 0
                self.create_timer(700)
                self.state += 1
                    
        elif self.state == 7:
            if e.name == "timer":
                self.create_timer(10000) # FIXME à mesurer
                self.robot.forward(5000)
                self.state += 1
                self.logger.info("Petit en attente de positionnement de gros")

        elif self.state == 8:
            if e.name == "robot":
                self.robot.forward(-2500)
                self.state += 1
            elif e.name == "timer":
                self.logger.warning("Pas de réponse de gros !")
                self.robot.forward(-2500)
                self.state += 1

        elif self.state == 9:
            if e.name == "asserv" and e.type == "done":
                self.logger.info("Petit en position !")
                self.state = 0
