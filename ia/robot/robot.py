# -*-coding:UTF-8 -*
from math import cos, sin
import logging
import socket

from can import Can, Wifi, UI
from event_dispatcher import Event_dispatcher
from mathutils.types import Vertex

class Robot:
    def __init__(self, x, y, theta, dim_l, dim_r, dim_t, dim_b, ip_can="petit", port_can=7773, ip_robot="petit", port_robot=7780, ip_ui="r2d2", port_ui=7774):
        self.logger = logging.getLogger("robot")
        
        self.mission_prefix = self.__class__.__name__.lower().split('_')[0]
        
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
        
#        self.ip_can     = ip_can
#        self.port_can   = port_can
#        self.ip_robot   = ip_robot
#        self.port_robot = port_robot
#        self.ip_ui      = ip_ui
#        self.port_ui    = port_ui
        
        self.sock_can   = self.connect(ip_can, port_can)
        self.sock_robot = self.connect(ip_robot, port_robot)
        self.sock_ui    = self.connect(ip_ui, port_ui)
        
        self.dispatcher = Event_dispatcher(self.mission_prefix, self)
        
        
        self.msg_can    = Can (self.sock_can, self.dispatcher)
        self.msg_robot  = Wifi(self.sock_robot, self.dispatcher)
        self.msg_ui     =   UI(self.sock_ui, self.dispatcher)
        
        
        self.dispatcher.start()
        self.msg_can.start()
        self.msg_robot.start()
        self.msg_ui.start()
        
        
        
    def connect(self, ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
        except socket.error as message:
            if sock: 
                sock.close()
            sock = None # On est sûr de tout arréter 
            self.logger.critical("Impossible d'otenir une connection pour %s %d : %s" % (ip, port, message))
        return sock
    
    def stop(self):
        self.sock_can.shutdown(socket.SHUT_WR) 
        self.sock_can.close()


    def asserv(self, left_wheel_speed, right_wheel_speed, curt=False):
        curt_str = ""
        if curt:
            curt_str = " curt" # l'espace est important
        self.send_can("asserv speed %d %d%s" % (left_wheel_speed, right_wheel_speed, curt_str))
    
    def forward(self, dist):
        self.pos_target = self.pos + Vertex(dist*cos(self.theta), dist*sin(self.theta))
        #print("DEBUG: ", dir(self.missions["forward"]))
        self.missions["forward"].move_forward(dist)

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
    
    def move_direction(self, dist, direction):
        '''dist en 10e de mmm
           direction en 10e de degré'''
        drot = direction-self.theta
        if drot < -18000:
            rot = 36000 + drot
        if drot > 18000:
            drot = -36000 + drot
        
    # Retro comptabilité
    def set_position(self, pos):
        self.pos = pos
        self.send_can("odo set %d %d %d" % (self.pos.x/10, self.pos.y/10, self.theta))
        
    def set_x(self, x):
        self.pos.x = x
        self.send_can("odo set %d %d %d" % (self.pos.x/10, self.pos.y/10, self.theta))

    def set_y(self, y):
        self.pos.y = y
        self.send_can("odo set %d %d %d" % (self.pos.x/10, self.pos.y/10, self.theta))
        
    def set_theta(self, theta):
        self.theta = theta
        self.send_can("odo set %d %d %d" % (self.pos.x/10, self.pos.y/10, self.theta))
        
    
    def stop(self):
        self.send_can("asserv stop")

    def fix_forward(self, dist):
        '''Après un stop, on corrige notre position'''


    def __str__(self):
        return "x=%.2f cm, y=%.2f cm, theta=%.2f°" % (self.pos.x/100, self.pos.y/100, self.theta/100)
