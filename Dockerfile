FROM oracle/weblogic:12.2.1.2-generic

MAINTAINER Lagutin R.A. <rlagutin@mta4.ru>

ARG PROPERTIES_DIR_SOURCE
ARG SCRIPTS_DIR_SOURCE
ARG FILES_DIR_SOURCE

USER root

RUN yum -y --setopt=tsflags=nodocs install -y glibc glibc-common && yum clean all
RUN ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime

USER oracle

ENV LANG='ru_RU.UTF-8' LANGUAGE='ru_RU.UTF-8' LC_ALL='ru_RU.UTF-8'
# ENV LANG='en_US.UTF-8' LANGUAGE='en_US.UTF-8' LC_ALL='en_US.UTF-8'

ENV ORACLE_HOME="/u01/oracle" \
    CONFIG_JVM_ARGS="-Djava.security.egd=file:/dev/./urandom" \
    USER_MEM_ARGS="-Djava.security.egd=file:/dev/./urandom" \
    JAVA_OPTIONS="-Doracle.jdbc.fanEnabled=false -Dweblogic.StdoutDebugEnabled=false" \
    PROPERTIES_DIR="/u01/oracle/properties" \
    SCRIPTS_DIR="/u01/oracle/scripts" \
    FILES_DIR="/u01/oracle/files" \
    PATH="$PATH:${JAVA_HOME}/bin:/u01/oracle/oracle_common/common/bin:/u01/oracle/wlserver/common/bin:/u01/oracle/scripts"

COPY ${PROPERTIES_DIR_SOURCE:-properties}/* $ORACLE_HOME/properties/
COPY ${SCRIPTS_DIR_SOURCE:-scripts}/* $ORACLE_HOME/scripts/
COPY ${FILES_DIR_SOURCE:-files}/* $ORACLE_HOME/files/

USER root

RUN chown -R oracle:oracle $ORACLE_HOME/properties && chmod -R a+r $ORACLE_HOME/properties && \
    chown -R oracle:oracle $ORACLE_HOME/scripts && chmod -R a+xr $ORACLE_HOME/scripts && \
    chown -R oracle:oracle $ORACLE_HOME/files && chmod -R a+r $ORACLE_HOME/files

USER oracle

WORKDIR $ORACLE_HOME
CMD ["/u01/oracle/scripts/runWLS.sh"]
