#!/usr/bin/env bash
set -e

dc="docker-compose --ansi never"
dcr="$dc run --rm"

log_file="install_log-`date +'%Y-%m-%d_%H-%M-%S'`.txt"
exec &> >(tee -a "$log_file")

DOTENV_FILE='real_state/.env'

DID_CLEAN_UP=0

# the cleanup function will be called when some error happens or
# when the script ends
cleanup () {
  if [ "$DID_CLEAN_UP" -eq 1 ]; then
    return 0;
  fi
  echo "Cleaning up..."
  $dc stop &> /dev/null
  DID_CLEAN_UP=1
}
trap cleanup ERR INT TERM

echo "...Starting..."

RAM_AVAILABLE_IN_DOCKER=$(docker run --rm busybox free -m 2>/dev/null | awk '/Mem/ {print $2}');

# Compare dot-separated strings - based on https://stackoverflow.com/a/37939589/808368
function version () { echo "$@" | cut -f3 -dv | awk -F. '{ printf("%d%03d%03d", $1,$2,$3); }'; }

# Check if the file exist and if not, copy from the default template
function ensure_file_from_template {
  if [ -f "$1" ]; then
    echo "$1 already exists, good."
  else
    echo "Creating $1 from template..."
    cp -n $(echo "$1" | sed 's/\.[^.]*$/&.default/') "$1"
  fi
}

# Ensure nothing is working while we install/update
$dc down --rmi local --remove-orphans

echo ""
echo "Creating volumes for persistent storage..."
echo "Created $(docker volume create --name=real_state-database)."
echo "Created $(docker volume create --name=real_state-mongo)."

echo ""
ensure_file_from_template $DOTENV_FILE

echo ""
echo "Fetching and updating Docker images..."
echo ""

$dc pull

echo ""
echo "Building Docker images..."
echo ""
$dc build --force-rm --parallel
echo ""
echo "Docker images built."

cleanup

echo ""
echo "----------------"
echo "Installation finished! Run the following command to get backend running:"
echo ""
echo "  docker-compose up -d"
echo ""
