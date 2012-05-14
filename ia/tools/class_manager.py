# -*- coding: utf-8 -*-
'''
Created on 27 avr. 2012
'''
import os
def class_loader(path):
    path = os.path.relpath(path, os.getcwd())
    path = os.path.normpath(path)
    classes = []
    files = os.listdir(path)
    is_package = '__init__.py' in files
    
    for file in files:
        file_path   = os.path.join(path,file)
        module_name =  path.replace("/", ".")
        if (os.path.isfile(file_path) and is_package and 
            file.endswith('.py') and file != '__init__.py'):
            mod = __import__('.'.join([module_name, file[:-3]]), fromlist=[file[:-3]])
            classes.extend([getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type)])

        elif os.path.isdir(file_path):
            classes.extend(class_loader(file_path))

    return classes
