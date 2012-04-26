# -*-coding:UTF-8 -*

from missions.Mission import Mission

class MissionRecalage(Mission):

    def __init__(self):
        Mission.__init__(self, "Recalage")

    def processEvent(self, event):
        if self.state == 0:
            # état0 = aller vers le bord le plus proche
            if event.name() == "OdoEvent":
                if event.type == "mute":
                    print("odo mutted !")
                elif event.type == "unmute":
                    print("odo unmutted !")
                elif event.type == "set":
                    print("odo set ",event.value)
            if event.name() == "BumpEvent":
                if event.state == 1:
                    # set odo = ...
                    self.state = 1 # terminé




