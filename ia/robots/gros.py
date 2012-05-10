# -*- coding: utf-8 -*-

from mathutils.types import Vertex

class PetitRobot:

    def __init__(self):

        self.name = "gros"

        # dimension du robot
        self.dimensions = { "left": 1290, "right": 1290,
                "front": 1190, "back": 920 }

        # position *initial* du robot
        self.pos = Vertex(-12000, -7000)
        # direction *initial* du robot
        self.rot = 0

        # paramètre de la tourelle
        self.turret = { "left": 12, "right": 8, "front": 40 }

        # paramètre par défaut des sockets
        # (utilisé par IA si pas de valeur spécifié)

        # socket can
        self.can_ip = "gros"
        self.can_port = 7777
        # socket interface graphique
        self.ui_ip = "gros"
        self.ui_port = 7779
        # socket inter-robot
        self.inter_ip = "gros"
        self.inter_port = 7780
