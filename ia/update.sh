echo " Usage ./update.sh <petit|gros>"
for line in `git status | grep modified | cut -d ':' -f 2 | cut -f 4 -d ' '`; do scp $line root@$1:/home/ia; done
