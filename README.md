## Docker: docker.weblogic-adminserver-app

Compiled Docker image: https://hub.docker.com/r/rlagutinhub/docker.weblogic-adminserver-app

>	* Oracle WebLogic 12.2.1.2-generic autoconfig (only first running) domain without cluster (only AdminServer) include deploying datasources, libraries, applications.
>	* Support run on Docker Standalone and Docker Swarm Mode
>	* Base image oraclelinux:7-slim

FYI https://github.com/oracle/docker-images

***

#### Prepare


Docker Image Oracle Linux 7 with Oracle Server JRE:
> FYI https://github.com/rlagutinhub/docker.oraclejava

```console
# get git oracle docker repo
git clone https://github.com/rlagutinhub/docker.weblogic-adminserver-app.git

# download Oracle Server JRE (example Java server-jre 1.8.0.172)
# http://download.oracle.com/otn/java/jdk/8u172-b11/a58eab1ec242421181065cdc37240b08/server-jre-8u172-linux-x64.tar.gz
cp server-jre-8u172-linux-x64.tar.gz ~/docker.weblogic-adminserver-app/distib/OracleJava/

# create docker image OracleJava (all required packages installed from oracle repo yum.oracle.com):
cd ~/docker.weblogic-adminserver-app/distib/OracleJava/
./build.sh

# result
docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
oracle/serverjre 8 fca1db36746d 5 days ago 280MB # base image + server jre
oraclelinux 7-slim 874477adb545 2 weeks ago 118MB # base image
```

Docker Image Oracle WebLogic 12.2.1.2-generic:
* Required Docker Image Oracle Linux 7 with Oracle Server JRE

```console
# get git oracle docker repo
git clone https://github.com/rlagutinhub/docker.weblogic-adminserver-app.git

# download weblogic 12.2.1.2 generic (https://www.oracle.com/middleware/technologies/weblogic-server-downloads.html)
cp fmw_12.2.1.2.0_wls_Disk1_1of1.zip ~/docker.weblogic-adminserver-app/distib/OracleWebLogic/12.2.1.2/

# create docker image weblogic:12.2.1.2-generic (all required packages installed from oracle repo yum.oracle.com)
cd ~/docker.weblogic-adminserver-app/distib/OracleWebLogic/
./buildDockerImage.sh -v 12.2.1.2 -g -s

# result
docker image ls
REPOSITORY          TAG                       IMAGE ID            CREATED             SIZE
oracle/weblogic     12.2.1.2-generic          eaaf52392276        5 days ago          2.78GB  # base image + server jre + wls
oracle/serverjre    8                         fca1db36746d        5 days ago          280MB # base image + server jre
oraclelinux         7-slim                    874477adb545        2 weeks ago         118MB # base image

# example run
mkdir -p ~/docker/properties; cat <<EOF >  ~/docker/properties/domain.properties
username=weblogic
password=welcome1
EOF

# For wls 12.2.1.2 to set the DOMAIN_NAME, you must set both DOMAIN_NAME and DOMAIN_HOME.
docker run -dit \
 --name wls-app \
 --network bridge \
 -p 7001:7001/tcp -p 9002:9002/tcp \
 -v /root/docker/properties:/u01/oracle/properties \
 -e ADMINISTRATION_PORT_ENABLED=true -e DOMAIN_HOME=/u01/oracle/user_projects/domains/docker_domain -e DOMAIN_NAME=docker_domain \
 oracle/weblogic:12.2.1.2-generic

docker ps -a
docker logs wls-app --follow
```
***

#### JPA support

* JPA (Java Persistent API) 2.1 it is automatically enabled on WebLogic 12.2.X but on WebLogic 12.1.3 JPA 2.1 has to be enabled manually Enabling JPA 2.1 in WebLogic Server 12.1.3 [link](https://github.com/oracle/docker-images/blob/master/OracleWebLogic/samples/1213-domain/container-scripts/commEnv.sh) [link](https://docs.oracle.com/middleware/1213/wls/EJBAD/using_toplink.htm#EJBAD1309) [link](https://www.oracle.com/webfolder/technetwork/tutorials/obe/fmw/wls/12c/01-06-004-JavaEE7andWebLogicServer/javaee7.html#section1)

#### Properties


```vim properties/domain_settings.properties```

* recommend ADMINISTRATION_PORT_ENABLED=true (admin console access only from other port with force ssl)

```console
[Base]
keys=base
base.domain_name=MTA4RU
base.admin_name=AdminServer
base.admin_listen_port=7001
base.production_mode=prod
base.administration_port_enabled=true
base.administration_port=9002
base.admin_console_enabled=true
base.derby_enabled=false
```

* Use only strong password 12-14 symbols (https://en.wikipedia.org/wiki/Password_strength)

```console
[Security]
keys=sec
sec.username=weblogic
sec.password=welcome1
```

* Java settings are applied via env variables (setDomainEnv.sh not modifaed)

```console
[Java]
keys=java
java.user_mem_args=-Xms1024m -Xmx1024m -Djava.security.egd=file:/dev/./urandom
java.java_options=-Dweblogic.configuration.schemaValidationEnabled=false -Dfile.encoding=UTF-8 -DCID_SHORT=${CID}- -Xdebug -Xrunjdwp:transport=dt_socket,address=1044,server=y,suspend=n -Djava.io.tmpdir=${ORACLE_HOME}/tmp/mta4ru/${CID}
```

* Move wls logs to single folder ${ORACLE_HOME}/Logs (the new location of the logs is not in DOMAIN_HOME, because if you use the mount volume, there will be an error files acl permission deny at creating domain)
* Add prefix docker ContainerID to wls logs filename (example AdminServer-123456789abc.log)
* Modify rotation settings for wls logs by file size and file count

```console
[Logging]
keys=admin access datasource diagnostic domain
admin.path=/Servers/AdminServer/Log/AdminServer
admin.file=/u01/oracle/logs/mta4ru/AdminServer.log
admin.fileMinSize=10000
admin.fileCount=50
admin.rotateLogOnStartup=True
access.path=/Servers/AdminServer/WebServer/AdminServer/WebServerLog/AdminServer
access.file=/u01/oracle/logs/mta4ru/access.log
access.fileMinSize=10000
access.fileCount=50
access.rotateLogOnStartup=True
datasource.path=/Servers/AdminServer/DataSource/AdminServer/DataSourceLogFile/AdminServer
datasource.file=/u01/oracle/logs/mta4ru/datasource.log
datasource.fileMinSize=10000
datasource.fileCount=50
datasource.rotateLogOnStartup=True
diagnostic.path=/Servers/AdminServer/ServerDiagnosticConfig/AdminServer
diagnostic.file=/u01/oracle/logs/mta4ru/diagnostic_images
diagnostic.fileMinSize=null
diagnostic.fileCount=null
diagnostic.rotateLogOnStartup=null
domain.path=/Log/MTA4RU
domain.file=/u01/oracle/logs/mta4ru/base_domain.log
domain.fileMinSize=10000
domain.fileCount=50
domain.rotateLogOnStartup=True
```

* Support wlst offline and online configuring datasources.

```console
[DataSources]
keys=example1 example2
example1.url=jdbc:oracle:thin:@db.example.com:1521:example1
example1.user=example
example1.password=example
example1.Name=dsExample1
example1.jndiName=jdbc/dsExample1
example1.GlobalTransactionsProtocol=EmulateTwoPhaseCommit
example1.driver=oracle.jdbc.xa.client.OracleXADataSource
example1.MaxCapacity=50
example1.ConnectionCreationRetryFrequencySeconds=10
example1.TestTableName=SQL SELECT 1 FROM DUAL
example1.XaSetTransactionTimeout=True
example1.XaTransactionTimeout=7200
example2.url=jdbc:oracle:thin:@db.example.com:1521:example2
example2.user=example
example2.password=example
example2.Name=dsExample2
example2.jndiName=jdbc/dsExample2
example2.GlobalTransactionsProtocol=None
example2.driver=oracle.jdbc.OracleDriver
example2.MaxCapacity=50
example2.ConnectionCreationRetryFrequencySeconds=10
example2.TestTableName=SQL SELECT 1 FROM DUAL
example2.XaSetTransactionTimeout=null
example2.XaTransactionTimeout=null
```

* Support wlst offline and online deploying libraries and applications.
* When you offline (not online) deploy application (not library) to WebLogic, in the Admin Console the application' deployment type will be listed as "UNKNOWN" instead of "Web Application". This issue has no affect on your application.

```console
[Deployments]
keys=jaxrs hello
jaxrs.name=jax-rs#2.0@2.22.1.0
jaxrs.type=Library
jaxrs.sourcePath=/u01/oracle/wlserver/common/deployable-libraries/jax-rs-2.0.war
jaxrs.securityDDModel=DDOnly
hello.name=hello
hello.type=AppDeployment
hello.sourcePath=/u01/oracle/files/hello.war
hello.securityDDModel=DDOnly
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
# default graceful stop-timeout 10s then forcestop (kill -9)
docker run -dit --stop-timeout 120 --name wls-app --network bridge -p 7001:7001/tcp -p 9002:9002/tcp oracle/weblogic:12.2.1.2-generic_custom; docker logs --follow wls-app
```
***

#### Run on Docker Swarm Mode
* For mount source `mkdir -p /data/{logs,tmp}` on docker host required `chmod -R 0777 /data/{logs,tmp}`

```docker stack deploy --compose-file docker-compose.yml wls-hello```

```console
version: '3.7'
services:
  app:
    image: rlagutinhub/docker.weblogic-adminserver-app:12.2.1.2-generic_custom
    networks:
       - proxy
    volumes:
      - /data/logs:/u01/oracle/logs:rw
      - /data/tmp:/u01/oracle/tmp:rw
    configs:
      - source: hello_domain_settings.properties.2019-09-05
        target: /u01/oracle/properties/domain_settings.properties
    stop_grace_period: 2m
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
        # - "traefik.frontend.rule=Host:hello.example.com,hello.test.example.com;AddPrefix:/hello;"
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
configs:
  hello_domain_settings.properties.2019-09-05:
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
