# -*- coding: utf-8 -*-
'''
Created on 12 mai 2012
'''

class Robot:
    '''Le but est de pouvoir faire depuis n'importe quelle classe
    Robot.attribut que je veux, sans que la classe ait besoin de savoir
    si on doit utiliser PetitRobot ou GrosRobot
    '''
    
    _vrille = 0
    
    @classmethod
    def copy_from(self, robot):
        '''inconvnient de cette mthode : c'est une copie  l'instant t
        de robot. Si une instance de robot est modifie par erreur,
        les attributs de classe de Robot ne sont plus  jour'''

        for attr in robot.__dict__:
            if attr[0] != "_":
                setattr(Robot, attr, robot.__dict__[attr])
   
        if robot.side == "red":
            Robot._vrille = -robot.__dict__['_vrille']
        else:
            Robot._vrille = robot.__dict__['_vrille']

    
    def vrille():
        if Robot.side == "red":
            return -Robot._vrille
        else:
            return Robot._vrille
        
        

