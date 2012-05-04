# -*-coding:UTF-8 -*
from math import cos, sin
import logging
from mathutils.types import Vertex

class Robot:
    def __init__(self, x, y, theta, dim_l, dim_r, dim_t, dim_b):
        self.logger = logging.getLogger("robot")
        
        self.pos = Vertex(x, y) # 10e de mm
        self.theta = theta # centidegree

        self.action = None #forwarding, rotating 
        self.pos_target = None # à court terme
        self.theta_target = None

        # Dimmensions du robot, left, right, bottom, top
        # L'origine du repère et le point médian entre les deux roues
        self.dim_l = dim_l
        self.dim_r = dim_r
        self.dim_b = dim_b
        self.dim_t = dim_t
        
        self.msg_can   = None
        self.msg_robot = None


    def asserv(self, left_wheel_speed, right_wheel_speed, curt=False):
        curt_str = ""
        if curt:
            curt_str = " curt" # l'espace est important
        self.send_can("asserv speed %d %d%s" % (left_wheel_speed, right_wheel_speed, curt_str))
    
    def forward(self, dist):
        self.pos_target = self.pos + Vertex(dist*cos(self.theta), dist*sin(self.theta))
        self.send_can("asserv dist %d" % dist)

    def rotate(self, dtheta):
        self.send_can("asserv rot %d" % dtheta)
        
    def get_theta(self):
        '''Retourne la direction en radian'''
        return self.theta/36000*6.28319
    
    def send_can(self, msg):
        if self.msg_can != None:
            self.msg_can.sender(msg)
        else:
            self.logger.error("Robot : msg_can is None, cannot send %s" % msg)
        
    # Retro comptabilité
    def set_position(self, pos):
        self.pos = pos
        self.send_can("odo set %d %d %d" % (self.pos.x, self.pos.y, self.theta))
        
    def set_x(self, x):
        self.pos.x = x
        self.send_can("odo set %d %d %d" % (self.pos.x, self.pos.y, self.theta))

    def set_y(self, y):
        self.pos.y = y
        self.send_can("odo set %d %d %d" % (self.pos.x, self.pos.y, self.theta))
        
    def set_theta(self, theta):
        self.theta = theta
        self.send_can("odo set %d %d %d" % (self.pos.x, self.pos.y, self.theta))
        
    
    def stop(self):
        self.send_can("asserv stop")

    def fix_forward(self, dist):
        '''Après un stop, on corrige notre position'''


    def __str__(self):
        return "x=%.2f cm, y=%.2f cm, theta=%.2f°" % (self.pos.x/100, self.pos.y/100, self.theta/100)
