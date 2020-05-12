CURRENT_DIR=$(pwd)
USER="ubuntu"
cd "/home/${USER}/service_centre"
docker-compose up -d
cd "${CURRENT_DIR}"
