#! /usr/bin/python3

# Usage : ./convert.py fichier_a_convertir

import sys
fichier = sys.argv[1]
f = open(fichier, 'r')
l = f.readlines()
f2 = open(fichier.replace("ia/", "ia2/"), 'w')
for line in l:
   s=line.encode('ascii', 'ignore').decode("ascii")
   f2.write(str(s))
f2.close()

