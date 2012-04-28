# -*- coding: utf8 -*-

from mathutils.types import Segment

class Scene:
    '''Définit la scène, ses obstacles, robots ...'''
    # TODO: check des valeurs ici
    def __init__(self):
        '''L'origine du plateau est son centre de gravité
        Toutes les coordonnées sont en 10ème de mm'''
        
        # Ceci facilitera les changements d'échelle et d'origine
        dx = -15000
        dy = -10000
        s  = 1
        self.plateau = Plateau(Wall(0,0,15000,0), 
                               Wall(0,0,0,20000),
                               Wall(0,20000,30000,20000),            
                               Wall(30000,0,30000,20000))
        self.plateau.adjust(dx, dy, s)


        # coffre/câle du capitaine
        box_l = Obstacle(Wall(0,0,6400,0),
                         Wall(0,0,0,7500,0),
                         Wall(0,7500,6400,7500),
                         Wall(6400,0,6400,7500))
        box_r= Obstacle(Wall(26400,0,30000,0),
                        Wall(26400,0,26400,7500,0),
                        Wall(26400,7500,30000,7500),
                        Wall(30000,0,30000,7500))


        # Totem gauche de centre de gravité en 11000,10000
        tgx=11000
        tgy=10000
        totem_l = Obstacle(Wall(tgx-125,tgy-125,tgx+125,tgy-125),
                           Wall(tgx-125,tgy-125,tgx-125,tgy+125),
                           Wall(tgx-125,tgy+125,tgx+125,tgy+125),
                           Wall(tgx+125,tgy-125,tgx+125,tgy+125))
        # Totem droit de centre de gravité ...
        tgx=19000
        tgy=10000
        totem_r = Obstacle(Wall(tgx-125,tgy-125,tgx+125,tgy-125),
                           Wall(tgx-125,tgy-125,tgx-125,tgy+125),
                           Wall(tgx-125,tgy+125,tgx+125,tgy+125),
                           Wall(tgx+125,tgy-125,tgx+125,tgy+125))
        


        self.obstacles = [box_l, box_r, totem_l, totem_r]
        for obstacle in self.obstacles:
            obstacle.adjust(dx, dy, s)

class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.segment = Segment(x1, y1, x2, y2)
        # unités en 10e de mm

    def adjust(self, dx, dy, scaling):
        self.segment *= scaling
        self.segment.translate(dx, dy)        


class Obstacle:
    def __init__(self, bottom, left, top, right):
        self.bottom = bottom
        self.left = left
        self.top = top
        self.right = right
    def adjust(self, dx, dy, scaling):
        for att in ["bottom","left", "top", "right"]:
            # Cette façon (__dict__) nuit-elle aux performances ? 
            self.__dict__[att].adjust(dx, dy, scaling)


class Plateau(Obstacle):
    '''Plateau du jeu'''
    def __init__(self, bottom, left, top, right):
        super(self.__class__,self).__init__(bottom, left, top, right)

