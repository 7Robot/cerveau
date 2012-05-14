# -*- coding: utf-8 -*-

from mathutils.types import Vertex

class GrosRobot:

    def __init__(self):

        self.name = "gros"
        
        # Zone de dpart : violet|red  oui c'est con
        self.side = "violet"

        # dimension du robot
        self.dimensions = { "left": 1500, "right": 1500,
                "front": 1950, "back": 1050 }

        self.vrille = 500

        # position *initial* du robot
        self.pos = Vertex(-12000, -7000)
        # direction *initial* du robot
        self.rot = 0

        # paramtre de la tourelle
        self.turret = { "left": 17, "right": 15, "front": 70 }

        # paramtre par dfaut des sockets
        # (utilis par IA si pas de valeur spcifi)
        self.rangefinder = { 1: 2800, 2: 2800, 8: 2800 }

        # socket can
        self.can_ip = "gros"
        self.can_port = 7777
        # socket interface graphique
        self.ui_ip = "gros"
        self.ui_port = 7779
        # socket inter-robot
        self.inter_ip = "gros"
        self.inter_port = 7780
