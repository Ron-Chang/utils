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
RED_ON_YELLOW='\x1b[5;31;43m'
YELLOW_ON_T='\x1b[5;33;40m'

RED='\x1b[5;31;40m'
ON_RED='\x1b[5;30;41m'

SERVICE_NAME="`echo ${CONTAINER} | awk '{split($0,N,"_"); print N[1]"_service"}'`"
UP="${BLUE}${ON_BLUE} DOWN ${BLUE_ON_YELLOW} ${RESET}"
SERVICE="${ON_YELLOW} SERVICE ${YELLOW_ON_RED} ${ON_RED} ${SERVICE_NAME} ${RED} ${RESET}"
echo "${UP}${SERVICE}"
docker-compose -f "${HOME}/${SERVICE_NAME}/docker-compose.yml" down

