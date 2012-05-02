# -*- coding: utf-8 -*-
'''
Created on 30 avr. 2012
'''

from math import cos, sin
from mathutils.types import Vertex
from mathutils.geometry import angle, distance
from threading import Timer


            

class Simu_robot():
    '''Robot physiquement simulé qui répond aux commandes de l'IA'''
        
    def __init__(self, pos, theta, max_speed, max_acceleration, sensors=None):
        self.pos     = pos
        self.theta   = theta
        self.accel   = 0
        self.speed   = 0
        self.mspeed  = max_speed
        self.maccel  = max_acceleration
        self.daccel  = max_acceleration/10
        self.msteer  = 50;
        self.action  = None
        self.can     = None
        self.sensors = sensors
        if sensors == None:
            self.sensors = []
        for sensor in self.sensors:
            sensor.robot = self
            sensor.init()
        #self.regulator = Regulator(self)
        
    def get_theta(self):
        '''Retourne la direction en radian'''
        return self.theta/3600*6.28319
        
    def accelerate(self,  accel): #rate between -100 and 100
        self.speed = min(accel+self.speed,self.mspeed)

    def go_speed(self, speed, curt=False):
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
        dx = self.speed * cos(self.get_theta())
        dy = self.speed * sin(self.get_theta())
        self.pos.translate(dx, dy)
#        print(self.pos)
#        print(self.speed)
#        print(self.accel)
        
    def turn(self, steer):
        self.theta += steer
        if self.theta < 0:
            self.theta += 3600
        if self.theta > 3600:
            self.theta -= 3600
        #print("theta", self.theta)

    def turn_direction(self, d):
        dd = d - self.theta
        if dd < -1800:
            dd = 3600 + dd
        if dd > 1800:
            dd = -3600 + dd

        sign = 1
        if dd < 0:
            sign = -1
        # trop la flemme pour un PID
        if abs(dd) < 100: #10 deg
            self.turn(self.msteer / 100 * dd)
        else:
            self.turn(self.msteer * sign)
            
#    def run(self):
#        if self.action == "go_speed":
#            self.go_speed(self.wanted_speed, self.curt)
#        self.move()
            
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
                
    def run(self):
        for sensor in self.sensors:
            sensor.run()

class Simu_regulator(Simu_robot):
    '''Pattern decorator, peut assigner autant de "cartes d'extension" 
    à un robot, il restera un robot'''
    def __init__(self, robot):
        self.__dict__ = robot.__dict__.copy()
        self.robot = robot
        self.fun  = None
        self.args = None
    def asserv_dist(self, dist):
        print("pos", self.pos)
        self.fun  = self.reach_vertex
        self.args = (Vertex(dist*cos(self.get_theta()), 
                           dist*sin(self.get_theta())) \
                    + self.pos,)
        print ("target", Vertex(dist*cos(self.get_theta()), 
                           dist*sin(self.get_theta())) \
                    + self.pos)
        timer = Timer(0.05, self.run, [])
        timer.start()
        self.run()
         
    def asserv_rot(self, theta):
        self.fun = self.turn_direction
        self.args=(theta,)
        timer = Timer(0.05, self.run, [])
        timer.start()
        
    def asserv_speed(self, speed, curt=False):
        self.fun  = self.go_speed
        self.args = (speed, curt,)
#        timer = Timer(0.05, self.run, [])
#        timer.start()
        self.run()
    
    def run(self):
        self.robot.run()
        if self.fun != None and self.args != None:
            self.fun(*self.args)
            self.move()
#            timer = Timer(0.05, self.run, [])
#            timer.start()
        