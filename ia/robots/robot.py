# -*- coding: utf-8 -*-
'''
Created on 12 mai 2012
'''

class Robot:
    '''Le but est de pouvoir faire depuis n'importe quelle classe
    Robot.attribut que je veux, sans que la classe ait besoin de savoir
    si on doit utiliser PetitRobot ou GrosRobot
    '''
    
    @classmethod
    def copy_from(self, robot):
        '''inconvénient de cette méthode : c'est une copie à l'instant t
        de robot. Si une instance de robot est modifiée par erreur,
        les attributs de classe de Robot ne sont plus à jour'''
        for attr in robot.__dict__:
            if attr[0] != "_":
                setattr(Robot, attr, robot.__dict__[attr])