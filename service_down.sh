CURRENT_DIR=$(pwd)
USER="ubuntu"
cd "/home/${USER}/service_centre"
docker-compose down
cd "${CURRENT_DIR}"
