# -*- coding: utf-8 -*-
'''
Created on 28 avr. 2012
'''

from math import atan2
from mathutils.types import Vertex, Vector, Segment


def angle(v1, v2):
    '''Retourne l'angle en radian entre v1 et v2'''
    dv = v2 - v1
    angle = atan2(dv.y, dv.x)
    return angle

def dot_product(v1,  v2):
    return v1.x*v2.x + v1.y*v2.y
    
def det(v1,  v2):
    '''Déterminant'''
    return v1.x*v2.y-v1.y*v2.x

def distance(v1, v2):
    '''Distance euclidienne entre 2 points'''
    return (v2-v1).norm()

def orientation(o, a, b):
    ''' 1 si le vecteur ob est à gauche de oa, 0 si alignés, -1 sinon
    @param o,a,b : Vector
    @return : un entier signé \in {-1,0,1}
    '''
    oa2  = Vector(-a.y+o.y,a.x-o.x)
    ob   = Vector(b.x-o.x,  b.y-o.y)
    prod = dot_product(oa2,ob)
    if prod > 0:
        return 1
    elif prod == 0:
        return 0
    else:
        return -1
    
def inSector(ab, ad, at):
    ''' Indique si le vecteur at est dans le secteur définit par (ab, ad)
    @param ab, ad, at: Vector
    @return: Boolean 
    '''
    o = Vertex(0,0)
    if orientation(o,ab,ad) >= 0:
        inSector =  (orientation(o,ab,at)>=0) and (orientation(o,at,ad)>=0)
    else:
        inSector =  not((orientation(o, ad, at) >= 0) and (orientation(o, at, ab) >= 0))
    return inSector


def segment_intersection(seg1, seg2):
    '''Retourne le point d'intersection de 2 segments'''
    if isinstance(seg1,Segment) and isinstance(seg2,Segment):
        seg1, seg2 = seg1.to_eq(), seg2.to_eq() 
    det = seg1.ax * (-seg2.ay) + seg1.ay * seg2.ax
    if det != 0:
        t = (seg1.ax * (seg2.by - seg1.by) - seg1.ay * (seg2.bx - seg1.bx))/det
        if t < 0 or t > 1:
            return None
        x = seg2.ax * t + seg2.bx
        y = seg2.ay * t + seg2.by
        return Vertex(x, y)
    else:
        return None
    
def is_segment_intersection(seg1, seg2):
    '''Renvoie True si seg1 et seg2 ont un point d'intersection
    mais ne calcule pas ce moint d'intersection (plus coûteux)'''
    a, b, c, t = seg1.vert1, seg1.vert2, seg2.vert1, seg2.vert2
    if (orientation(a,t,c)>=0):
        return (orientation(a,b,c)!=orientation(a,b,t)) and (orientation(b,a,t)>0) and (orientation(b,c,t)>0)
    else:
        return (orientation(a, b, c) != orientation(a, b, t)) and (orientation(b, a, t) <= 0) and (orientation(b, c, t) <= 0)
    
def distance2_vertex_segment(vert, seg):
    ''' Retourne la distance AU CARRÉ entre vert et seg
    Segment [a,b], vert=v'''
    av = Vector()
    bv = Vector()
    ab = seg.to_vector()
    av.vert2vert(seg.vert1, vert)
    bv.vert2vert(seg.vert2, vert)
    abav = ab * av
    abbv = ab * bv
    if abav*abbv >= 0:
        # Projection de v sur (a,b) n'appartient pas à [a,b]
        return min(av*av, bv*bv)
    else:
        return av*av - abav**2/(ab*ab) 
        
    