# -*- coding: utf-8 -*-

from mathutils.types import Vertex

class PetitRobot:

    def __init__(self):

        self.name = "petit"
        
        # Zone de dpart : violet|red (attribut de classe)
        self.side = "red"

        # dimension du robot
        self.dimensions = { "left": 1290, "right": 1290,
                "front": 1190, "back": 920 }

        self.vrille = 0

        # position *initial* du robot
        self.pos = Vertex(-12000, -7000)
        # direction *initial* du robot
        self.rot = 0

        # paramtre de la tourelle
        self.turret = { "left": 12, "right": 10, "front": 60 }

        # paramtre par dfaut des sockets
        # (utilis par IA si pas de valeur spcifi)
        self.rangefinder = { 1: 2800, 2: 2800, 8: 2800 }

        # socket can
        self.can_ip = "petit"
        self.can_port = 7773
        # socket interface graphique
        self.ui_ip = "petit"
        self.ui_port = 7774
        # socket inter-robot
        self.inter_ip = "petit"
        self.inter_port = 7780
