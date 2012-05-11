# SUpprime tous les __pycache__ et tous les .pyc

find -name "__pycache__" -exec rm -r "{}" \;
