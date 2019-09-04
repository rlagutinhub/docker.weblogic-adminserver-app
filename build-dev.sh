#!/bin/sh

scriptDir="$( cd "$(dirname $0)" && pwd)"; cd $scriptDir

# 1.rm
docker rm -f wls-app; docker image rm oracle/weblogic:12.2.1.2-generic_custom

# 2.app
./build-app.sh

# 3.image
./build.sh "properties" "scripts" "files" "Dockerfile"  "oracle/weblogic:12.2.1.2-generic_custom" "/root/docker/wls-app"

# 4.container
docker run -dit --name wls-app  --network bridge -p 7001:7001/tcp -p 9002:9002/tcp oracle/weblogic:12.2.1.2-generic_custom; docker logs --follow wls-app

