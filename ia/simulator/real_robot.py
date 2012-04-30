# -*- coding: utf-8 -*-
'''
Created on 30 avr. 2012
'''

from math import cos, sin
from mathutils.types import Vertex
from mathutils.geometry import angle, distance

class Regulator:
    def __init__(self, real_robot):
        self.real_robot = real_robot
        self.fun  = None
        self.args = None
    def asserv_dist(self, dist):
        self.fun  = self.real_robot.reach_vertex
        self.args = (Vertex(dist*cos(self.real_robot.theta), 
                           dist*sin(self.real_robot.theta)) \
                    + self.real_robot.pos,)
        self.run()
         
    def asserv_rot(self, theta):
        self.fun = self.real_robot.turn_direction
        self.args=(theta,)
        self.run()
        
    def asserv_speed(self, speed, curt=False):
        self.fun  = self.real_robot.go_speed
        self.args = (speed, curt,)
        self.run()
    
    def run(self):
        if self.fun != None and self.args != None:
            self.fun(*self.args)
            self.real_robot.move()
            

class Real_robot():
    '''Robot physiquement simulé qui répon aux commandes de l'IA'''
        
    def __init__(self, robot, max_speed, max_acceleration):
        self.pos    = Vertex(robot.pos.x, robot.pos.y)
        self.theta = robot.theta/36000*6.28319
        self.accel  = 0
        self.speed  = 0
        self.mspeed = max_speed
        self.maccel = max_acceleration
        self.daccel = max_acceleration/10
        self.msteer = 0.5;
        self.action = None
        
    def accelerate(self,  accel): #rate between -100 and 100
        self.speed = min(accel+self.speed,self.mspeed)

    def go_speed(self, speed, curt=False):
        print ("go speed", speed)
        self.wanted_speed = speed
        self.curt = curt
        self.prev_action = "go_speed"
        ds = speed - self.speed
        sign = 1
        if ds < 0:
            sign = -1
        
#        if speed == 0 and (abs(ds)+0.5) <= self.maccel:
#            # mode frein
#            self.speed = 0
#        else:
        if curt:
            self.accel = self.maccel
        else:
            self.accel = min(self.accel +  self.daccel, self.maccel)
        self.accelerate(sign * self.accel)
            
    def move(self):
        dx = self.speed * cos(self.theta)
        dy = self.speed * sin(self.theta)
        self.pos.translate(dx, dy)
        print(self.pos)
        print(self.speed)
        print(self.accel)
        
    def turn(self, steer):
        self.theta += steer
        if self.theta < 0:
            self.theta += 6.28319
        if self.theta > 6.28319:
            self.theta -= 6.28319

    def turn_direction(self, d):
        dd = d - self.theta
        if dd < -3.14159:
            dd = 6.28319 + dd
        if dd > 3.14159:
            dd = -6.28319 + dd

        sign = 1
        if dd < 0:
            sign = -1
        # trop la flemme pour un PID
        if abs(dd) < 0.785: #10 deg
            self.turn(self.msteer / 0.785 * dd)
        else:
            self.turn(self.msteer * sign)
            
    def run(self):
        if self.action == "go_speed":
            self.go_speed(self.wanted_speed, self.curt)
        self.move()
            
    def reach_vertex(self, goal):
        d = distance(goal, self.pos)
        ang = angle(self.pos, goal)
        diff = abs(ang - self.theta)
        if diff >= 3.14159:
            diff = 6.28319 - diff

        if d < 700:
            self.go_speed(0)
        elif self.speed == 0:
            self.go_speed(1)
            self.turn_direction(ang)
        elif diff > 0.15:
            self.go_speed(1)
            self.turn_direction(ang)
        elif diff > 1.5708:
            self.go_speed(0)
            self.turn_direction(ang)
        else:
            ticks = max(0,(d-250)) / self.speed # -5 = security distance
            if ticks > 0:
                self.go_speed(ticks * self.maccel)
                self.turn_direction(ang)
            else:
                self.go_speed(0)

