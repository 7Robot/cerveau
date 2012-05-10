# -*- coding: utf-8 -*-
'''
Created on 29 avr. 2012
'''


from mathutils.types import Vertex
from robot.small_robot import Small_robot
from robot.proxy_robot import Proxy_robot, Spy

class Observer:
    def update(self, type, event, *args):
        print(type, event, args, "notified!")

obs = Observer()

robot      = Small_robot()
robot_simu = Proxy_robot(robot)
Spy.add_observer(obs)

#robot_simu.test()
#robot_simu.x = 2
#print(robot_simu.x)
robot_simu.forward(10)
robot_simu.asserv(10, 10, True)
robot_simu.pos = Vertex()
#print(robot_simu.x)
print("pos", robot_simu.pos.x)
print("name", robot_simu.__class__.__name__)
print(dir(robot_simu))
print()
print(dir(robot))

