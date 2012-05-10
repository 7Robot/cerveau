# -*- coding: utf-8 -*-
'''
Created on 28 avr. 2012
'''

from ia import IA
from mathutils.types import Vertex, Vector
from simulator.simu import Simu
from simulator.simu_robot import Simu_robot
from simulator.sensors import Bump_sensor
from robot.proxy_robot import Proxy_robot
from scene import Scene
import threading

if __name__ == '__main__':
    
    scene = Scene()
    bump_sensors = Bump_sensor(scene, "back", Vertex(-1000, 0), 
                               Vector(-50, 0))
    robot = Simu_robot(3000-15000, 3000-10000,0, 200, 60)
    robot = Proxy_robot(robot)
    
    simu = Simu(robot, scene)
    ia = IA(robot, "localhost", 8773, "localhost", 7769)
    ia_thread = threading.Thread(None, ia.main, None, (), {})
    ia_thread.start()
    simu.main()