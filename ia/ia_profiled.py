#!/usr/bin/python3
# -*-coding: ascii -*

# Profiling de tous les threads avec Yappi
# http://code.google.com/p/yappi/

import sys
import yappi
from ia import IA

if __name__ == u"__main__":
       
    if len(sys.argv) < 2:
        print u"Usage: %s <nom_robot>" %sys.argv[0]
    
    yappi.start()
    ia = IA(sys.argv[1], **{u"can_ip" : u"petit", 
                        u"ui_ip": u"petit", 
                        u"inter_ip" : u"petit"})

    # on attend que tous les threads se terminent
    
    print u"Stopping the profiler"
    yappi.stop()
    
    yappi.print_stats()