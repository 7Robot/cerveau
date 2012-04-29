# -*- coding: utf-8 -*-
'''
Created on 29 avr. 2012
'''



from robot.small_robot import Small_robot
from robot.simu_robot import Simu_robot

class Observer:
    def update(self, event):
        print(event, "notified!")

obs = Observer()

robot      = Small_robot()
robot_simu = Simu_robot(robot)
Simu_robot.add_observer(obs)

robot_simu.test()
robot_simu.x = 2
print(robot_simu.x)
print(robot_simu.__class__.__name__)

