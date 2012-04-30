# -*- coding: utf8 -*-

from mathutils.types import Segment, Vertex

class Scene:
    '''Définit la scène, ses obstacles, robots ...'''
    # TODO: check des valeurs ici
    def __init__(self):
        '''L'origine du plateau est son centre de gravité
        Toutes les coordonnées sont en 10ème de mm'''
        
        # Ceci facilitera les changements d'échelle et d'origine
        self.dx = -15000
        self.dy = -10000
        self.s  = 1
        self.plateau = Plateau(Vertex(0,0), Vertex(30000,20000))
        self.plateau.adjust(self.dx, self.dy, self.s)


        # Totem gauche de centre de gravité en 11000,10000
        tgx=11000
        tgy=10000
        totem_l = Box(Vertex(tgx-1250,tgy-1250), Vertex(tgx+1250,tgy+1250))
        # Totem droit de centre de gravité ...
        tgx=19000
        tgy=10000
        totem_r = Box(Vertex(tgx-1250,tgy-1250), Vertex(tgx+1250,tgy+1250))


        self.obstacles = {"totem_left" : totem_l, 
                          "totem_right" : totem_r}
        for obstacle in self.obstacles.values():
            obstacle.adjust(self.dx, self.dy, self.s)
            
      

class Box:
    def __init__(self, corner1=Vertex(), corner2=Vertex()):
        self.corner1 = corner1
        self.corner2 = corner2

    def adjust(self, dx, dy, scaling):
        self.corner1 *= scaling 
        self.corner1.translate(dx, dy)
        self.corner2 *= scaling 
        self.corner2.translate(dx, dy)        
        
    def copy(self):
        return Box(self.corner1.copy(), self.corner2.copy())
    
    def to_segments(self):
        return [Segment(self.corner1, Vertex(self.corner2.x, self.corner1.y)),
                Segment(self.corner1, Vertex(self.corner1.x, self.corner2.y)),
                Segment(Vertex(self.corner1.x, self.corner2.y), self.corner2),
                Segment(Vertex(self.corner2.x, self.corner1.y), self.corner2),]
        
    def __str__(self):
        return "corner1: %s, corner2: %s" % (self.corner1, self.corner2)


class Plateau(Box):
    '''Plateau du jeu'''
    def __init__(self, corner1, corner2):
        super(self.__class__,self).__init__(corner1, corner2)

