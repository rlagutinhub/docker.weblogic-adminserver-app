Oracle WebLogic Server on Docker
=================================
These Docker configurations have been used to create the Oracle WebLogic Server (WLS) image. Providing this WLS image facilitates the configuration and environment setup for DevOps users. This project includes the installation and creation of an empty WebLogic Server domain (an Administration Server only). These Oracle WebLogic Server 12.2.1.2 images are based on Oracle Linux and Oracle JRE 8 (Server).

The certification of Oracle WebLogic Server on Docker does not require the use of any file presented in this repository. Customers and users are welcome to use them as starters, and customize, tweak, or create from scratch, new scripts and Dockerfiles.

For more information on the certification, please see the [Oracle WebLogic Server on Docker certification whitepaper](http://www.oracle.com/technetwork/middleware/weblogic/overview/weblogic-server-docker-containers-2491959.pdf) and [The WebLogic Server Blog](https://blogs.oracle.com/WebLogicServer/) for updates.

## How to build and run
This project offers sample Dockerfiles for Oracle WebLogic Server 12cR2 (12.2.1.2). It provides at least one Dockerfile for the 'developer' distribution, a second Dockerfile for the 'generic' distribution. To assist in building the images, you can use the [`buildDockerImage.sh`](dockerfiles/buildDockerImage.sh) script. See below for instructions and usage.

The `buildDockerImage.sh` script is a utility shell script that performs MD5 checks and is an easy way for beginners to get started. Expert users are welcome to directly call `docker build` with their prefered set of parameters.

### Building Oracle WebLogic Server Docker install images
**IMPORTANT:** You must download the binary of Oracle WebLogic Server and put it in place (see `.download` files inside `dockerfiles/<version>`). The WebLogic image extends the Oracle JRE Server 8 image. You must either build the image by using the Dockerfile in [`../../../OracleJava/java8`](https://github.com/oracle/docker-images/tree/master/OracleJava/java-8) or pull the latest image from the [Oracle Container Registry](https://container-registry.oracle.com) or the [Docker Store](https://store.docker.com).

Before you build, select the version and distribution for which you want to build an image, then download the required packages (see `.download` files) and locate them in the folder of your distribution version of choice. Then, from the `dockerfiles` folder, run the `buildDockerImage.sh` script as root.

        $ sh buildDockerImage.sh
        Usage: buildDockerImage.sh -v [version] [-d | -g ] [-s]
        Builds a Docker Image for Oracle WebLogic Server.

        Parameters:
           -v: version to build. Required.
           Choose : 12.2.1.2
           -d: creates image based on 'developer' distribution
           -g: creates image based on 'generic' distribution
           -c: enables Docker image layer cache during build
           -s: skips the MD5 check of packages

        * select one distribution only: -d, or -g

        LICENSE UPL 1.0

        Copyright (c) 2014-2018 Oracle and/or its affiliates. All rights reserved.

**IMPORTANT:** The resulting images will have a single server domain (Administration Server only), by default.


  1. To build the `12.2.1.2`image, from `dockerfiles`, call:

        `$ sh buildDockerImage.sh -v 12.2.1.2 -d`

  2. Verify that you now have this image in place with:

        `$ docker images`

### Running a single server domain from the image
The WebLogic Server install image (built above) allows you to run a container with a single WebLogic Server domain.  This makes it extremely simple to deploy applications and any resource the application might need.

#### Providing the Administration Server user name and password
The user name and password must be supplied in a `domain.properties` file located in a HOST directory that you will map at Docker runtime with the `-v` option to the image directory `/u01/oracle/properties`. The properties file enables the scripts to configure the correct authentication for the WebLogic Administration Server.

The format of the `domain.properties` file is key=value pair:

	username=myadminusername
	password=myadminpassword

**Note**: Oracle recommends that the `domain.properties` file be deleted or secured after the container and the WebLogic Server are started so that the user name and password are not inadvertently exposed.

#### Start the container
Start a container from the image created in step 1.
You can override the default values of the following parameters during runtime with the `-e` option:

      * `ADMIN_NAME`                  (default: `AdminServer`)
      * `ADMIN_LISTEN_PORT`           (default: `7001`)
      * `DOMAIN_NAME`                 (default: `base_domain`)
      * `DOMAIN_HOME`                 (default: `/u01/oracle/user_projects/domains/base_domain`)
      * `ADMINISTRATION_PORT_ENABLED` (default: `true`)
      * `ADMINISTRATION_PORT`         (default: `9002`)

**NOTE**: For security, the Administration port 9002 is enabled by default, before running the container in WebLogic 12.2.1.2 the patch 27117282 must be applied. Please download the patch and apply it after you have built the 12.2.1.2 image. You can follow the sample https://github.com/oracle/docker-images/tree/master/OracleWebLogic/samples/12213-patch to see how to patch. An alternative is to not enable Administration port when you issue the docker run command, set `ADMINISTRTATION_PORT_ENABLED` to false. If you intend to run these images in production, then you must change the Production Mode to `production`. To set the `DOMAIN_NAME`, you must set both `DOMAIN_NAME` and `DOMAIN_HOME`.

	$docker run -d -p 7001:7001 -p 9002:9002  -v `HOST PATH where the domain.properties file is`:/u01/oracle/properties -e ADMINISTRATION_PORT_ENABLED=true -e DOMAIN_HOME=/u01/oracle/user_projects/domains/abc_domain -e DOMAIN_NAME=abc_domain oracle/weblogic:12.2.1.2-developer

Run the WLS Administration Console:

        $ docker inspect --format '{{.NetworkSettings.IPAddress}}' <container-name>

In your browser, enter `https://xxx.xx.x.x:9002/console`. Your browser will request that you accept the Security Exception. To avoid the Security Exception, you must update the WebLogic Server SSL configuration with a custom identity certificate.

## Choose your Oracle WebLogic Server distribution

This project hosts two configurations (depending on the Oracle WebLogic Server version) for building Docker images with WebLogic Server 12c.

 * Quick Install Developer Distribution

   - For more information on the Oracle WebLogic Server 12cR2 Quick Install Developer Distribution, see [WLS Quick Install Distribution for Oracle WebLogic Server 12.2.1.2.0](http://download.oracle.com/otn/nt/middleware/12c/wls/12212/README.txt).


 * Generic Distribution

   - For more information on the Oracle WebLogic Server 12cR2 Generic Full Distribution, see [WebLogic Server 12.2.1.2 Documentation](http://docs.oracle.com/middleware/12212/wls/index.html).

## Samples for Oracle WebLogic Server domain creation
To give users an idea of how to create a WebLogic domain and cluster from a custom Dockerfile which extends the WebLogic Server install image, we provide a few samples for 12c versions of the developer distribution. For an example, look at the `12212-domain` sample.

## Copyright
Copyright (c) 2014-2018 Oracle and/or its affiliates. All rights reserved.
