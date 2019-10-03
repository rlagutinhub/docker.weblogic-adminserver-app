# Oracle Java on Docker
```
```
This repository contains a sample Docker configuration to facilitate installation and environment setup for DevOps users. This project includes a Dockerfile for Server JRE 8 based on Oracle Linux with include <b>package rootfiles</b> (for enable root bash profile).
>	* Base image oraclelinux:7-slim

FYI [oracle/docker-images](https://github.com/oracle/docker-images/tree/master/OracleJava)

***

Oracle Java Server JRE provides the features from Oracle Java JDK commonly required for server-side applications (i.e. Running a Java EE application server). For more information about Server JRE, visit the [Understanding the Server JRE blog entry](https://blogs.oracle.com/java-platform-group/understanding-the-server-jre) from the Java Product Management team.

## Building the Java 8 (Server JRE) base image
[Download Server JRE 8](http://www.oracle.com/technetwork/java/javase/downloads/server-jre8-downloads-2133154.html) `.tar.gz` file and drop it inside the folder `../OracleJava/java-8`.

Build it using:

```
$ cd ../OracleJava/java-8
$ docker build -t oracle/serverjre:8 .
```
