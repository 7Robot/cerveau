#!/usr/bin/python3
# -*-coding: ascii -*

# Profiling de tous les threads avec Yappi
# http://code.google.com/p/yappi/

import sys
import yappi
from ia import IA

if __name__ == "__main__":
       
    if len(sys.argv) < 2:
        print("Usage: %s <nom_robot>" %sys.argv[0])
    
    yappi.start()
    ia = IA(sys.argv[1], **{"can_ip" : "petit", 
                        "ui_ip": "petit", 
                        "inter_ip" : "petit"})

    # on attend que tous les threads se terminent
    
    print("Stopping the profiler")
    yappi.stop()
    
    yappi.print_stats()