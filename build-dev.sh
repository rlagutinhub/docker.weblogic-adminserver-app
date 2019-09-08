#!/bin/sh

scriptDir="$(cd "$(dirname $0)" && pwd)"; cd $scriptDir

# 1.rm
docker rm -f wls-app.$(date +%F); docker image rm oracle/weblogic:12.2.1.2-generic_custom:$(date +%F)

# 2.app
./build-app.sh

# 3.image
./build.sh "properties" "scripts" "files" "Dockerfile" "oracle/weblogic:12.2.1.2-generic_custom:$(date +%F)" "."

# 4.container
docker run -dit --name wls-app.$(date +%F) --network bridge -p 7001:7001/tcp -p 9002:9002/tcp oracle/weblogic:12.2.1.2-generic_custom:$(date +%F); docker logs --follow wls-app.$(date +%F)
