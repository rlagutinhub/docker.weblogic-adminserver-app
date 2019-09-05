## Docker: docker.weblogic-adminserver-app

Compiled Docker image: https://hub.docker.com/r/rlagutinhub/docker.weblogic-adminserver-app

-	Docker - Oracle WebLogic 12.2.1.2-generic autoconfig domain without cluster (only AdminServer and User Application).
-	Support run on Docker Standalone and Docker Swarm Mode
-	Base image oraclelinux:7-slim

FYI https://github.com/oracle/docker-images

#### Prepare


Docker Image Oracle Linux 7 with Oracle Server JRE:

```console
cd ~

# get git oracle docker repo
git clone https://github.com/oracle/docker-images.git

# download Oracle Server JRE (example Java server-jre 1.8.0.172)
# http://download.oracle.com/otn/java/jdk/8u172-b11/a58eab1ec242421181065cdc37240b08/server-jre-8u172-linux-x64.tar.gz
cp server-jre-8u172-linux-x64.tar.gz ~/docker-images/OracleJava/java-8/

# create docker image OracleJava (all required packages installed from oracle repo yum.oracle.com):
cd ~/docker-images/OracleJava/java-8
./build.sh

# result
docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
oracle/serverjre 8 fca1db36746d 5 days ago 270MB # base image + server jre
oraclelinux 7-slim 874477adb545 2 weeks ago 118MB # base image
```

Docker Image Oracle WebLogic 12.2.1.2-generic:
* Required Docker Image Oracle Linux 7 with Oracle Server JRE

```console
cd ~

# get git oracle docker repo
git clone https://github.com/oracle/docker-images.git

# download weblogic 12.2.1.2 generic (ttps://www.oracle.com/technetwork/middleware/ias/downloads/wls-main-097127.html)
# fmw_12.2.1.2.0_wls_Disk1_1of1.zip # http://download.oracle.com/otn/nt/middleware/12c/12212/fmw_12.2.1.2.0_wls_Disk1_1of1.zip
cp fmw_12.2.1.2.0_wls_Disk1_1of1.zip ~/docker-images/OracleWebLogic/dockerfiles/12.2.1.2/

# create docker image weblogic:12.2.1.2-generic (all required packages installed from oracle repo yum.oracle.com)
~/docker-images/OracleWebLogic/dockerfiles/buildDockerImage.sh -v 12.2.1.2 -g -s

# result
docker image ls
REPOSITORY          TAG                       IMAGE ID            CREATED             SIZE
oracle/weblogic     12.2.1.2-generic          eaaf52392276        5 days ago          2.77GB  # base image + server jre + wls
oracle/serverjre    8                         fca1db36746d        5 days ago          270MB # base image + server jre
oraclelinux         7-slim                    874477adb545        2 weeks ago         118MB # base image
```


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

