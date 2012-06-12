# -*- coding: utf-8 -*-

from mathutils.types import Vertex

class PetitRobot(object):

    def __init__(self):

        self.name = u"petit"
        
        # Zone de dpart : violet|red (attribut de classe)
        self.side = u"red"

        # dimension du robot
        self.dimensions = { u"left": 1290, u"right": 1290,
                u"front": 1190, u"back": 920 }

        self._vrille = 0

        # position *initial* du robot
        self.pos = Vertex(-12000, -7000)
        # direction *initial* du robot
        self.rot = 0

        # paramtre de la tourelle
        self.turret = { u"left": 12, u"right": 10, u"front": 60 }

        # paramtre par dfaut des sockets
        # (utilis par IA si pas de valeur spcifi)
        self.rangefinder = { 1: 2800, 2: 2800, 8: 2800 }

        # socket can
        self.can_ip = u"petit"
        self.can_port = 7773
        # socket interface graphique
        self.ui_ip = u"petit"
        self.ui_port = 7774
        # socket inter-robot
        self.inter_ip = u"petit"
        self.inter_port = 7780
