CURRENT_DIR=$(pwd)
USER="`whoami`"
cd "/Users/${USER}/spyder_platform_service"
docker-compose down
cd "${CURRENT_DIR}"
