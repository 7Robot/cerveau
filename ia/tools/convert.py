#! /usr/bin/python3

# Usage : ./convert.py fichier_a_convertir

import sys
from io import open
fichier = sys.argv[1]
f = open(fichier, u'r')
l = f.readlines()
f2 = open(fichier.replace(u"ia/", u"ia2/"), u'w')
for line in l:
   s=line.encode(u'ascii', u'ignore').decode(u"ascii")
   f2.write(unicode(s))
f2.close()

