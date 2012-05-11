# Usages : 
#
# nc r2d2 7773 | ./colored.sh
# cat log_file | ./colored.sh

while read line; do
    # Logging
    if `echo $line | grep -q 'CRITIC'` ; then
        printf "\033[1;41;33m%s\033[0m\n" "$line"
    elif `echo $line | grep -q 'ERROR'` ; then
        printf "\033[1;41;37m%s\033[0m\n" "$line"
    elif `echo $line | grep -q 'WARNING'` ; then
        printf "\033[1;43;30m%s\033[0m\n" "$line"
    elif `echo $line | grep -q 'INFO'` ; then
        printf "\033[1;40;37m%s\033[0m\n" "$line"

    # Can messages
    elif `echo $line | grep -iq 'odo'` ; then
        printf "\033[1;40;37m%s\033[0m\n" "$line"
    elif `echo $line | grep -iq 'asserv'` ; then
        printf "\033[1;42;30m%s\033[0m\n" "$line"
    elif `echo $line | grep -iq 'battery'` ; then
        printf "\033[1;41;37m%s\033[0m\n" "$line"
    elif `echo $line | grep -iq 'bump'` ; then
        printf "\033[1;43;30m%s\033[0m\n" "$line"
    elif `echo $line | grep -iq 'rangefinder'` ; then
        printf "\033[1;46;32m%s\033[0m\n" "$line"
    elif `echo $line | grep -iq 'turret'` ; then
        printf "\033[1;44;32m%s\033[0m\n" "$line"
    



    else
        echo $line
    fi
done;
