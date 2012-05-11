# usage : ./server.sh <port:int>

while [ 1 ]; do nc -l -p $1; done
