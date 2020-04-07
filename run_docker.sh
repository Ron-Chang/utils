path="`pwd`"
CONTAINER_NAME=${1:-`basename ${path}`}
clear
echo "\x1b[1;37m:: \x1b[1;34mSTART\x1b[1;37m :: \x1b[1;31m RUNNING [${CONTAINER_NAME}]\x1b[0m"
docker exec -it ${CONTAINER_NAME} bash -l

# if [ "`ping -c 1 some_ip_here`" ]
# then
#   echo "Host found"
#   sleep 1
# else
#   docker-compose -f rebuild.yml up
# fi

# while [ $(docker inspect --format "{{json .State.Status }}" credit_phpmyadmin) != "running" ]
# do
#     # printf "Wait\n"
#     docker inspect --format "{{json .State }}" credit_phpmyadmin
#     sleep 1
# done
# docker-compose -f rebuild.yml up

# until nc -z -v -w30 0.0.0.0 8080
# do
#   echo "Waiting for database connection..."
#   sleep 2
# done
# docker-compose -f rebuild.yml up
