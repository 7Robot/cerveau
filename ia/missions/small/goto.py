# -*- coding: utf-8 -*-
'''
Created on 5 mai 2012
'''

from events.internal import GotoDoneEvent

from missions.mission import Mission
class GotoMission(Mission):
    def __init__(self, robot):
        super(self.__class__,self).__init__(robot)
        self.state = "repos"

    def disable(self):
        self.state = "repos"

    def move_to(self):
        if self.state == "repos":
            # première étape : prendre la direction du point cible
            self.state = "directioning"
            self.missions["rotate"].take_direction()

    def process_event(self, event):
        if self.state == "directioning":
            if event.name == "rotatedone":
                # 2ième étape : avancé jusqu'au point cible
                self.state = "forwarding"
                self.missions["forward"].move_forward()
        if self.state == "forwarding":
            if event.name == "forwarddone":
                # 3ième étape : s'orienté dans la direction demandé
                if self.robot.rot_target == None:
                    # Aucune direction demandé, c'est fini
                    self.robot.rot_target = self.robot.rot
                    self.state = "repos"
                    self.dispatch.add_event(GotoDoneEvent())
                else:
                    # On effectue la rotation
                    self.state = "rotating"
                    self.missions["rotate"].rotate()

        if self.state == "rotating":
            if event.name == "rotatedone":
                # C'était la dernière étape
                self.state = "repos"
                self.dispatch.add_event(GotoDoneEvent())

