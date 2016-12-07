#!/bin/bash
RED="\033[0;31m"
NC="\033[0m"

build_images() {
  docker-compose "${@}" build --no-cache
  docker-compose "${@}" up -d 
}

prompt() {
  read -e -p "$1 [$2]: " var
  echo ${var:-$2}
}

#export DOCKERHOST=$(ifconfig | grep -E "([0-9]{1,3}\.){3}[0-9]{1,3}" | grep -v 127.0.0.1 | awk '{ print $2 }' | cut -f2 -d: | head -n1)
export DOCKERHOST=$(docker-machine ip vmw)
export PYPI_SERVER_HOST=${PYPI_SERVER_HOST:-$(prompt "PyPI server host" "$DOCKERHOST")}
export PYPI_SERVER_SCHEME=${PYPI_SERVER_SCHEME:-$(prompt "PyPI server scheme" "http://")}
export PYPI_SERVER_PORT=${PYPI_SERVER_PORT:-$(prompt "PyPI server scheme" "8080")}
type=${BASH_ARGV[0]:-dev}

echo -e "${RED}Building ${type} environment...${NC}"
build_images "-f" "layouts/${type}.yml" 
