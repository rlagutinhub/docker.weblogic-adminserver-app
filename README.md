docker build -f Dockerfile -t oracle/weblogic:12.2.1.2-generic_custom .

docker rm -f wls-app; docker image rm oracle/weblogic:12.2.1.2-generic_custom
docker rm -f wls-app; docker image rm oracle/weblogic:12.2.1.2-generic_custom; docker build -f Dockerfile -t oracle/weblogic:12.2.1.2-generic_custom .
docker run -dit --name wls-app  --network bridge -p 7001:7001/tcp -p 9002:9002/tcp oracle/weblogic:12.2.1.2-generic_custom; docker logs --follow wls-app

docker run -dit --name wls-app  --network bridge -p 7001:7001/tcp -p 9002:9002/tcp oracle/weblogic:12.2.1.2-generic_custom bash

docker run -dit --name wls-app  --network bridge -p 7001:7001/tcp -p 9002:9002/tcp oracle/weblogic:12.2.1.2-generic
docker run -dit --name wls-app  --network bridge -p 7001:7001/tcp -p 9002:9002/tcp oracle/weblogic:12.2.1.2-generic bash

docker image ls
docker image rm 
docker ps -a
docker logs --follow wls-app
docker rm -f wls-app
docker exec -it wls-app bash

docker rm -f wls-app; docker image rm oracle/weblogic:12.2.1.2-generic_custom


cat /proc/*/status | grep -i -e 'name' -e 'pid'

----
https://localhost:9002/console/
http://localhost:7001/console/

