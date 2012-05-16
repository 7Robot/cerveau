# -*- coding: utf-8 -*-
'''
Created on 10 mai 2012
'''

from ia import IA


if __name__ == "__main__":
    ia = IA("petit", **{"can_ip" : "localhost", "can_port": 7777, "ui_ip": "localhost", "ui_port": 7778})
