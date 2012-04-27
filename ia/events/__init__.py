#-*- coding: utf-8 -*-

import os, sys
from class_manager import *


path = os.path.dirname(os.path.abspath(__file__))

classes = class_loader(path)
for cls in classes:
    setattr(sys.modules[__name__], cls.__name__, cls)


