# -*- coding: utf-8 -*-
'''
Created on 30 avr. 2012
'''

from math import cos, sin
from mathutils.types import Vertex
from mathutils.geometry import angle, distance
from threading import Timer
from robot.robot import Robot

class Asserv:
    def __init__(self, robot):
        self.robot = robot
        self.fun  = None
        self.args = None
    def asserv_dist(self, dist):
        print("pos", self.robot.pos)
        self.fun  = self.robot.reach_vertex
        self.args = (Vertex(dist*cos(self.robot.get_theta()), 
                           dist*sin(self.robot.get_theta())) \
                    + self.pos,)
        print ("target", Vertex(dist*cos(self.robot.get_theta()), 
                           dist*sin(self.robot.get_theta())) \
                    + self.pos)
        timer = Timer(0.05, self.robot.run, [])
        timer.start()
        
         
    def asserv_rot(self, theta):
        self.fun = self.robot.turn_direction
        self.args=(theta+self.robot.theta,)
        timer = Timer(0.05, self.robot.run, [])
        timer.start()
        
    def asserv_speed(self, speed, curt=False):
        self.fun  = self.robot.go_speed
        self.args = (speed, curt,)
#        timer = Timer(0.05, self.run, [])
#        timer.start()
        
    
    def run(self):
        self.robot.run()
        if self.fun != None and self.args != None:
            self.fun(*self.args)
            self.robot.move()
#            timer = Timer(0.05, self.run, [])
#            timer.start()
        
            

class Simu_robot(Robot):
    '''Robot physiquement simulé qui répond aux commandes de l'IA'''
        
    def __init__(self, x, y, theta, max_speed, max_acceleration):
        super(self.__class__, self).__init__(x, y, theta, 0,0,0,0)
        self.accel   = 0
        self.speed   = 0
        self.mspeed  = max_speed
        self.maccel  = max_acceleration
        self.daccel  = max_acceleration/10
        self.msteer  = 500;
        self.action  = None
        self.msg_can = None
        self.asserv  = Asserv(self)
        self.sensors = []
        
        
        for sensor in self.sensors:
            sensor.robot = self
            sensor.init()
        #self.regulator = Regulator(self)
        
        
    def add_sensor(self, sensor):
        self.sensors.append(sensor)
        sensor.robot = self
        sensor.init()
        
        
    def get_theta(self):
        '''Retourne la direction en radian'''
        return self.theta/36000*6.28319
        
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
            self.theta += 36000
        if self.theta > 36000:
            self.theta -= 36000
        #print("theta", self.theta)

    def turn_direction(self, d):
        dd = d - self.theta
        if dd < -18000:
            dd = 36000 + dd
        if dd > 18000:
            dd = -36000 + dd

        sign = 1
        if dd < 0:
            sign = -1
        # trop la flemme pour un PID
        if abs(dd) < 1000: #10 deg
            self.turn(self.msteer / 1000 * dd)
        elif abs(dd) > 50:
            self.turn(self.msteer * sign)
        else:
            self.asserv.func = None
            self.asserv.args = None
            self.send_can("asserv done")
            
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
        if self.asserv.fun != None and self.asserv.args != None:
            self.asserv.fun(*self.asserv.args)
            self.move()
