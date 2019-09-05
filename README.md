## Docker: docker.weblogic-adminserver-app

Compiled Docker image: https://hub.docker.com/r/rlagutinhub/docker.weblogic-adminserver-app

>	* Docker - Oracle WebLogic 12.2.1.2-generic autoconfig domain without cluster (only AdminServer and User Application).
>	* Support run on Docker Standalone and Docker Swarm Mode
>	* Base image oraclelinux:7-slim

FYI https://github.com/oracle/docker-images

***

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
***

#### Properties


```vim properties/domain_base.properties # domain base settings```
* recommend ADMINISTRATION_PORT_ENABLED=true (admin console access only from other port with force ssl)

```console
DOMAIN_NAME=MTA4RU
ADMIN_NAME=AdminServer
ADMIN_LISTEN_PORT=7001
PRODUCTION_MODE=prod
ADMINISTRATION_PORT_ENABLED=true
ADMINISTRATION_PORT=9002
```

```vim properties/domain_security.properties # domain security settings```
* Use only strong password 12-14 symbols (https://en.wikipedia.org/wiki/Password_strength)

```console
username=weblogic
password=welcome1
```

```vim properties/domain_modify.properties # domain modify logging settings```
* Move to single folder ${ORACLE_HOME}/user_projects/domains/${DOMAIN_NAME}/Logs
* Add prefix docker ContainerID to logs file name (example AdminServer-123456789abc.log)
* Modify rotation settings by file size and file count

```console
log.admin.path=/Servers/AdminServer/Log/AdminServer
log.admin.file=../../logs/mta4ru/AdminServer.log
log.admin.fileMinSize=10000
log.admin.fileCount=50
log.admin.rotateLogOnStartup=True
log.access.path=/Servers/AdminServer/WebServer/AdminServer/WebServerLog/AdminServer
log.access.file=../../logs/mta4ru/access.log
log.access.fileMinSize=10000
log.access.fileCount=50
log.access.rotateLogOnStartup=True
log.datasource.path=/Servers/AdminServer/DataSource/AdminServer/DataSourceLogFile/AdminServer
log.datasource.file=../../logs/mta4ru/datasource.log
log.datasource.fileMinSize=10000
log.datasource.fileCount=50
log.datasource.rotateLogOnStartup=True
log.diagnostic.path=/Servers/AdminServer/ServerDiagnosticConfig/AdminServer
log.diagnostic.file=../../logs/mta4ru/diagnostic_images
log.diagnostic.timeout=1
log.domain.path=/Log/MTA4RU
log.domain.file=../../logs/mta4ru/base_domain.log
log.domain.fileMinSize=10000
log.domain.fileCount=50
log.domain.rotateLogOnStartup=True
```

```vim properties/domain_java.properties # domain java settings```
* Java settings are applied via env variables (setDomainEnv.sh not modifaed)

```console
USER_MEM_ARGS=-Xms1024m -Xmx2048m -XX:MaxPermSize=1024m -Djava.security.egd=file:/dev/./urandom
JAVA_OPTIONS=-Dweblogic.configuration.schemaValidationEnabled=false -Dfile.encoding=UTF-8 -Xdebug -Xrunjdwp:transport=dt_socket,address=1044,server=y,suspend=n -Djava.io.tmpdir=/tmp/
```

```vim properties/domain_app.properties # domain app settings required for installation```

```console
app.name=hello
app.path=/u01/oracle/files
app.file=hello.war
```
***

#### Run on Docker Standalone


```./build-dev.sh # automate```

or manual:
```
# 1.rm
docker rm -f wls-app; docker image rm oracle/weblogic:12.2.1.2-generic_custom

# 2.app
./build-app.sh

# 3.image
./build.sh "properties" "scripts" "files" "Dockerfile"  "oracle/weblogic:12.2.1.2-generic_custom" "/root/docker/wls-app"

# 4.container
docker run -dit --name wls-app  --network bridge -p 7001:7001/tcp -p 9002:9002/tcp oracle/weblogic:12.2.1.2-generic_custom; docker logs --follow wls-app
```
***


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

