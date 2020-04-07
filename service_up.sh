CURRENT_DIR=$(pwd)
USER="`whoami`"
cd "/Users/${USER}/spyder_platform_service"
docker-compose up -d
cd "${CURRENT_DIR}"
