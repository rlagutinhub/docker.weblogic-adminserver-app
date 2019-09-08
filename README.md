## Docker: docker.weblogic-adminserver-app

Compiled Docker image: https://hub.docker.com/r/rlagutinhub/docker.weblogic-adminserver-app

>	* Oracle WebLogic 12.2.1.2-generic autoconfig domain without cluster (only AdminServer and User Application) only on first start docker container.
>	* Support run on Docker Standalone and Docker Swarm Mode
>	* Base image oraclelinux:7-slim

FYI https://github.com/oracle/docker-images

***

#### Prepare


Docker Image Oracle Linux 7 with Oracle Server JRE:

```console
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
* Move wls logs to single folder ${ORACLE_HOME}/Logs (the new location of the logs is not in DOMAIN_HOME, because if you use the mount volume, there will be an error files acl permission deny at creating domain)
> https://github.com/rlagutinhub/docker.weblogic-adminserver-app/blob/master/scripts/runWLS.sh#L159
* Add prefix docker ContainerID to wls logs filename (example AdminServer-123456789abc.log)
* Modify rotation settings for wls logs by file size and file count

```console
log.admin.path=/Servers/AdminServer/Log/AdminServer
log.admin.file=/u01/oracle/logs/mta4ru/AdminServer.log
log.admin.fileMinSize=10000
log.admin.fileCount=50
log.admin.rotateLogOnStartup=True
log.access.path=/Servers/AdminServer/WebServer/AdminServer/WebServerLog/AdminServer
log.access.file=/u01/oracle/logs/mta4ru/access.log
log.access.fileMinSize=10000
log.access.fileCount=50
log.access.rotateLogOnStartup=True
log.datasource.path=/Servers/AdminServer/DataSource/AdminServer/DataSourceLogFile/AdminServer
log.datasource.file=/u01/oracle/logs/mta4ru/datasource.log
log.datasource.fileMinSize=10000
log.datasource.fileCount=50
log.datasource.rotateLogOnStartup=True
log.diagnostic.path=/Servers/AdminServer/ServerDiagnosticConfig/AdminServer
log.diagnostic.file=/u01/oracle/logs/mta4ru/diagnostic_images
log.diagnostic.timeout=1
log.domain.path=/Log/MTA4RU
log.domain.file=/u01/oracle/logs/mta4ru/base_domain.log
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

automate:
```console
./build-dev.sh
```

or manual:
```console
# 1.rm
docker rm -f wls-app; docker image rm oracle/weblogic:12.2.1.2-generic_custom

# 2.app
./build-app.sh

# 3.image
./build.sh "properties" "scripts" "files" "Dockerfile" "oracle/weblogic:12.2.1.2-generic_custom" "."

# 4.container
docker run -dit --name wls-app --network bridge -p 7001:7001/tcp -p 9002:9002/tcp oracle/weblogic:12.2.1.2-generic_custom; docker logs --follow wls-app
```
***

#### Run on Docker Swarm Mode
* For logs mount source on docker host required chmod -R 0777 /logs

```docker stack deploy --compose-file docker-compose.yml wls-hello```

```console
version: '3.7'
services:
  app:
    image: rlagutinhub/docker.weblogic-adminserver-app:12.2.1.2-generic_custom
    networks:
       - proxy
    volumes:
      - /logs:/u01/oracle/logs:rw
    configs:
      - source: hello_domain_base.properties.2019-09-05
        target: /u01/oracle/properties/domain_base.properties
      - source: hello_domain_security.properties.2019-09-05
        target: /u01/oracle/properties/domain_security.properties
      - source: hello_domain_modify.properties.2019-09-05
        target: /u01/oracle/properties/domain_modify.properties
      - source: hello_domain_java.properties.2019-09-05
        target: /u01/oracle/properties/domain_java.properties
      - source: hello_domain_app.properties.2019-09-05
        target: /u01/oracle/properties/domain_app.properties
    deploy:
      # mode: global
      replicas: 1
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
        # order: stop-first
      restart_policy:
        condition: on-failure
        delay: 10s
        max_attempts: 3
        window: 120s
      labels:
        # https://docs.traefik.io/configuration/backends/docker/#on-containers
        - "traefik.enable=true"
        - "traefik.port=7001"
        # - "traefik.weight=10"
        - "traefik.frontend.rule=Host:hello.example.com,hello.test.example.com"
        # - "traefik.frontend.rule=Host:hello.example.com,hello.test.example.com;PathPrefixStrip:/app"
        - "traefik.frontend.entryPoints=http"
        # - "traefik.frontend.entryPoints=http,https"
        # - "traefik.frontend.headers.SSLRedirect=true"
        # - "traefik.frontend.auth.basic.users=root:$$apr1$$mLRjS/wr$$QqrALWNDgW9alDmnb9DeK1"
        # - "traefik.backend.loadbalancer.stickiness=true"
        - "traefik.backend.loadbalancer.method=wrr"
      placement:
        constraints:
          # - node.role == manager
          # - node.role == worker
          - node.labels.hello == true
networks:
  proxy:
    external: true
# volumes:
  # logs:
    # external: true
configs:
  hello_domain_base.properties.2019-09-05:
    external: true
  hello_domain_security.properties.2019-09-05:
    external: true
  hello_domain_modify.properties.2019-09-05:
    external: true
  hello_domain_java.properties.2019-09-05:
    external: true
  hello_domain_app.properties.2019-09-05:
    external: true
```
***

#### Result


> * https://localhost:9002/console/ # if ADMINISTRATION_PORT_ENABLED=true
> * http://localhost:7001/console/ # if ADMINISTRATION_PORT_ENABLED=false
> * http://localhost:7001/hello/ # application

![alt text](https://github.com/rlagutinhub/docker.weblogic-adminserver-app/blob/master/screen1.png)
![alt text](https://github.com/rlagutinhub/docker.weblogic-adminserver-app/blob/master/screen2.png)
![alt text](https://github.com/rlagutinhub/docker.weblogic-adminserver-app/blob/master/screen3.png)

https://raw.githubusercontent.com/rlagutinhub/docker.weblogic-adminserver-app/master/example.run.log
