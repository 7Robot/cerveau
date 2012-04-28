# -*- coding: utf-8 -*-
'''
Created on 28 avr. 2012
'''

import math

class Vertex(object):
    '''Point 2D
    Attention, suite a un calcul on peut avoir des flottants !'''
     
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def int_values(self):
        return (int(self.x), int(self.y))
        
    def translate(self, dx, dy):
        self.x += dx
        self.y += dy
                    
        
    def __eq__(self, v): 
        return v!=None and (self.x==v.x) and (self.y==v.y)
        
    def __str__(self):
        return "Vertex: x=%.1%, y=%.1%", self.x, self.y
    
class Vector(Vertex):        
    def __init__(self, x=0, y=0):
        super(self.__class__, self).__init__(x, y)

        
    def vert2vert(self, v1, v2):
        '''Create a vector going from v1 to v2'''
        self.x = v2.x-v1.x
        self.y = v2.y-v1.y
    
    def normalize(self):
        '''||v|| = 1'''
        n = self.norm()
        if n != 0:
            self.x/=n
            self.y/=n
        else:
            self.x=0
            self.y=0
                
    def norm(self):
        return math.hypot(self.x, self.y)
    
    
    def __abs__(self):
        return self.norm()
    
    def __add__(self, v):  
        return Vector(self.x+v.x, self.y+v.y)
    
    def __mul__(self, c):
        if isinstance(c,Vector):
            return self.x*c.x+self.y*c.y
        else:
            Vector(c*self.x, c*self.y)
    
    def __neg__(self): 
        return Vertex(-self.x, -self.y)
    
    def __sub__(self, v): 
        return Vector(self.x-v.x, self.y-v.y)
    
    
    def __str__(self):
        return "Vector: x=%.1%, y=%.1%", self.x, self.y
        
        
        
class Segment:
    def __init__(self, vert1, vert2):
        self.vert1 = vert1
        self.vert2 = vert2
        
    def scale(self, k):
        self.vert1 *= k
        self.vert2 *= k
        
    def to_eq(self):
        ax = self.vert2.x - self.vert1.x
        ay = self.vert2.y - self.vert1.y
        bx = self.vert1.x
        by = self.vert1.y
        return SegmentEq(ax, bx, ay, by)
        
    def translate(self, dx, dy):
        self.vert1.translate(dx, dy)
        self.vert2.translate(dx, dy)
        
    def __str__(self):
        return ("Segment: v1: (x=%.1f, y=%.1f), v2: (x=%.1f, y=%.1f)" 
              % (self.vert1.x, self.vert1.y, self.vert2.x, self.vert2.y))
        
    
class SegmentEq:
    '''Représentation paramétrique d'un segment
    x(t) = ax * t + bx
    y(t) = ay * t + by
    t \in [0..1]
    '''
    def __init__(self, ax, bx, ay, by):
        self.ax = ax
        self.bx = bx
        self.ay = ay
        self.by = by
        
    def __str__(self):
        return ("SegmentEq: ax=%.1f, bx=%.1f, ay=%.1f, by=%.1f" 
              % (self.ax, self.bx, self.ay, self.by))

