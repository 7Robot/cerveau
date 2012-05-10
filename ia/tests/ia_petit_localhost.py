# -*- coding: utf-8 -*-
'''
Created on 10 mai 2012
'''

from ia import IA


m = __import__("mathutils")
print(m.__dict__.keys())
print(getattr(m, "types"))

if __name__ == "__main__":
    ia = IA("petit", **{"can_ip" : "localhost", "ui_ip": "localhost"})
    