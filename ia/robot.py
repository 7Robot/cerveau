# -*-coding:UTF-8 -*

from mathutils.types import Vertex 

class Robot:
    def __init__(self, x, y, theta, dim_l, dim_r, dim_t, dim_b):
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



    
    def forward(self, dist):
        pass

    def rotate(self, dtheta):
        pass

    def stop(self):
        pass

    def fix_forward(self, dist):
        '''Après un stop, on corrige notre position'''


    def __str__(self):
        return "x= %.2f cm, y= .2f cm, theta=%.2f°" % (self.pos.x/100, self.pos.y/100, self.theta/100)


