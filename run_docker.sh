PROJECT_PATH="`git rev-parse --show-toplevel`"
PROJECT_NAME="`basename ${PROJECT_PATH}`"
CONTAINER=${1:-$PROJECT_NAME}

RESET='\x1b[0m'

BLUE='\x1b[5;34;40m'
ON_BLUE='\x1b[5;30;44m'
BLUE_ON_YELLOW='\x1b[3;34;43m'

YELLOW='\x1b[5;33;40m'
ON_YELLOW='\x1b[5;30;43m'
YELLOW_ON_RED='\x1b[5;33;41m'

RED='\x1b[5;31;40m'
ON_RED='\x1b[5;30;41m'

RUN="${BLUE}  ${ON_BLUE}   RUN ${BLUE_ON_YELLOW} ${RESET}"
CONTAINER_NAME="${ON_YELLOW}   CONTAINER ${YELLOW_ON_RED} ${ON_RED} ${CONTAINER} ${RED} ${RESET}"
INFO="${RUN}${CONTAINER_NAME}"
clear
echo $INFO
docker exec -it ${CONTAINER} bash -l

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
