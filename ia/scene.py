# -*-

class Scene:
    '''Définit la scène, ses obstacles, robots ...'''
    # TODO: check des valeurs ici
    def __init__(self):
        
        self.plateau = Plateur(Wall(0,0,30000,0), 
                          Wall(0,0,0,20000),
                          Wall(0,20000,30000,20000),            
                          Wall(30000,0,30000,20000))

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
        


        self.obstacle = [box_l, box_r, totem_l, totem_r]
        

class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1 # 10e de mm
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2


class Obstacle:
    def __init__(self, bottom, left, top, right):
        self.bottom = bottom
        self.left = left
        self.top = top
        self.right = right



class Plateau(Obstacle):
    '''Plateau de jeu'''
    def __init__(self, bottom, left, top, right):
        Obstacle.__init__(bottom, left, top, right)


