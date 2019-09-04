#!/bin/sh

if [ "$#" -eq 6 ]; then

    if [ ! -d "$1" ]; then echo 'ROPERTIES_DIR_SOURCE not exist: '$1; exit 1; fi
    if [ ! -d "$2" ]; then echo 'SCRIPTS_DIR_SOURCE not exist: '$2; exit 1; fi
    if [ ! -d "$3" ]; then echo 'FILES_DIR_SOURCE not exist: '$3; exit 1; fi
    if [ ! -f "$4" ]; then echo 'DOCKERFILE not exist: '$4; exit 1; fi
    if [ ! -d "$6" ]; then echo 'ROOT_DIR not exist: '$6; exit 1; fi
    cd $6

    docker build \
     --build-arg PROPERTIES_DIR_SOURCE="$1" \
     --build-arg SCRIPTS_DIR_SOURCE="$2" \
     --build-arg FILES_DIR_SOURCE="$3" \
     -f "$4" \
     -t "$5" \
     .

else
    echo 'Usage: '$0' [ROPERTIES_DIR_SOURCE] [SCRIPTS_DIR_SOURCE] [FILES_DIR_SOURCE] [DOCKERFILE] [IMAGENAME] [ROOT_DIR]'
    echo
    echo 'Example:'
    echo '       '$0' "properties" "scripts" "files" "Dockerfile" "oracle/weblogic:12.2.1.2-generic_custom" "/root/docker/wls-app"'
    exit 0
fi
