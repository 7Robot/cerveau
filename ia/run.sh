#!/bin/sh

export PYTHONPATH=".":$PYTHONPATH

python3 ./ia.py `hostname` > ia.out 2>ia.err
