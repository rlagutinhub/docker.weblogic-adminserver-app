#!/bin/bash

# NAME:   RUNWLS.SH
# DESC:   RUN WLS
# DATE:   18-10-2019
# LANG:   BASH
# AUTHOR: LAGUTIN R.A.
# EMAIL:  RLAGUTIN@MTA4.RU

. ${SCRIPTS_DIR}/libraries.sh

########### SIGTERM handler ############
function _term() {

   echo "Stopping container."
   echo "SIGTERM received, shutting down the server!"
   # ${DOMAIN_HOME}/bin/stopWebLogic.sh

   # Shutdown domain
   # wlst.sh -skipWLSModuleScanning \
   #  -loadProperties ${DOM_PROPERTIES_FILE} \
   #  -loadProperties ${SEC_PROPERTIES_FILE} \
   #  ${SCRIPTS_DIR}/shutdown-wls-domain.py

   # Shutdown domain (connect t3 or t3s with DemoTrust cert allow)
   . ${DOMAIN_HOME}/bin/setDomainEnv.sh

   java \
    -Dweblogic.security.SSL.ignoreHostnameVerification=true \
    -Dweblogic.security.CustomTrustKeyStoreType="JKS" \
    -Dweblogic.security.TrustKeyStore=CustomTrust \
    -Dweblogic.security.CustomTrustKeyStoreFileName="${ORACLE_HOME}/wlserver/server/lib/DemoTrust.jks" \
    weblogic.WLST \
    -skipWLSModuleScanning \
    ${SCRIPTS_DIR}/shutdown-wls-domain.py -p ${DOM_PROPERTIES_FILE}

   retval=$?

   if [ "${DERBY_ENABLED}" == "true" ] ; then
      # . ${ORACLE_HOME}/wlserver/common/derby/bin/stopNetworkServer.sh  >"${DOMAIN_HOME}/derbyShutdown.log" 2>&1
      . ${WL_HOME}/common/derby/bin/stopNetworkServer.sh  >"${DOMAIN_HOME}/derbyShutdown.log" 2>&1
      echo "Derby server stopped."
   fi

   echo  "RetVal from Domain shutdown $retval"

   if [ $retval -ne 0 ]; then
      echo "Domain Shutdown Failed.. Please check the Domain Logs"
      exit 1
   else
      echo "Domain Shutdown Successfully.. Please check the Domain Logs"
      exit 0
   fi

}

########### SIGKILL handler ############
function _kill() {

   echo "SIGKILL received, shutting down the server!"
   kill -9 $childPID

}

# Set SIGTERM handler
trap _term SIGTERM

# Set SIGKILL handler
trap _kill SIGKILL

echo "Properties file"
echo "=========================="

# Get DOM_PROPERTIES_FILE
DOM_PROPERTIES_FILE=${PROPERTIES_DIR}/domain_settings.properties
echo $DOM_PROPERTIES_FILE
if [ ! -r "${DOM_PROPERTIES_FILE}" ]; then
    echo "A Domain properties file needs to be supplied."
    exit 1
fi

# Get DOMAIN_NAME
DOMAIN_NAME=$(_properties ${DOM_PROPERTIES_FILE} "Base" "base.domain_name")
if [ -z "${DOMAIN_NAME}" ]; then
    echo "The DOMAIN_NAME is blank. The DOMAIN_NAME must be set in the properties file."
    exit 1
fi

# Get ADMIN_NAME
ADMIN_NAME=$(_properties ${DOM_PROPERTIES_FILE} "Base" "base.admin_name")
if [ -z "${ADMIN_NAME}" ]; then
    echo "The ADMIN_NAME is blank. The ADMIN_NAME must be set in the properties file."
    exit 1
fi

# Get DERBY_ENABLED
DERBY_ENABLED=$(_properties ${DOM_PROPERTIES_FILE} "Base" "base.derby_enabled")
if [ -z "${DERBY_ENABLED}" ]; then
    echo "The DERBY_ENABLED is blank. The DERBY_ENABLED must be set in the properties file."
    exit 1
fi

# Get USERNAME
USER=$(_properties ${DOM_PROPERTIES_FILE} "Security" "sec.username")
if [ -z "${USER}" ]; then
    echo "The domain username is blank. The Admin username must be set in the properties file."
    exit 1
fi

# Get PASSWORD
PASS=$(_properties ${DOM_PROPERTIES_FILE} "Security" "sec.password")
if [ -z "${PASS}" ]; then
    echo "The domain password is blank.  The Admin password must be set in the properties file."
    exit 1
fi

echo
echo "Domain HOME"
echo "=========================="

# Define DOMAIN_HOME
export DOMAIN_HOME=${ORACLE_HOME}/user_projects/domains/${DOMAIN_NAME}
echo "Domain Home is:" $DOMAIN_HOME

echo
echo "Docker Container ID"
echo "=========================="

# Define Container ID
CID=$(cat /proc/self/cgroup | head -n 1 | cut -d '/' -f3 | cut -c 1-12)
if [ ! -z "$CID" ]; then
    export CID=$CID
    echo "Container ID is:" $CID
else
    echo "Container ID not defined."
    exit 1
fi

echo
echo "Configure Domain"
echo "=========================="

ADD_DOMAIN=1
# if [ ! -f ${DOMAIN_HOME}/servers/${ADMIN_NAME}/logs/${ADMIN_NAME}.log ]; then
if [ ! -f ${DOMAIN_HOME}/.keep_conf ]; then
    ADD_DOMAIN=0
else
    echo "Domain already configured is:" $DOMAIN_NAME
fi

if [ $ADD_DOMAIN -eq 0 ]; then

    # Create domain
    wlst.sh -skipWLSModuleScanning \
     ${SCRIPTS_DIR}/create-wls-domain.py -p ${DOM_PROPERTIES_FILE}

    retval=$?

    echo  "RetVal from Domain creation $retval"

    if [ $retval -ne 0 ]; then
       echo "Domain Creation Failed.. Please check the Domain Logs"
       exit 1
    fi

    # Create the security file to start the server(s) without the password prompt
    mkdir -p ${DOMAIN_HOME}/servers/${ADMIN_NAME}/security/
    echo "username=${USER}" >> ${DOMAIN_HOME}/servers/${ADMIN_NAME}/security/boot.properties
    echo "password=${PASS}" >> ${DOMAIN_HOME}/servers/${ADMIN_NAME}/security/boot.properties

    # Create Logs folder
    # mkdir -p ${DOMAIN_HOME}/logs/
    mkdir -p ${ORACLE_HOME}/logs/

    # Logging
    wlst.sh -skipWLSModuleScanning \
     ${SCRIPTS_DIR}/logging-wls-domain.py -p ${DOM_PROPERTIES_FILE} -c ${CID}

    retval=$?

    echo  "RetVal from Domain modify $retval"

    if [ $retval -ne 0 ]; then
       echo "Logging Failed.. Please check the Domain Logs"
       exit 1
    fi

    # DataSources
    wlst.sh -skipWLSModuleScanning \
     ${SCRIPTS_DIR}/datasources-wls-domain.py -p ${DOM_PROPERTIES_FILE} -m offline # offline or online

    retval=$?

    echo  "RetVal from Domain modify $retval"

    if [ $retval -ne 0 ]; then
       echo "DataSources Failed.. Please check the Domain Logs"
       exit
    fi

    # Libraries
    # cp ${FILES_DIR}/lib_mbeans-current.jar ${ORACLE_HOME}/wlserver/server/lib/mbeantypes/lib_mbeans.jar

    # Deployments
    wlst.sh -skipWLSModuleScanning \
     ${SCRIPTS_DIR}/deployments-wls-domain.py -p ${DOM_PROPERTIES_FILE} -m offline # offline or online

    retval=$?

    echo  "RetVal from Domain modify $retval"

    if [ $retval -ne 0 ]; then
       echo "Deployments Failed.. Please check the Domain Logs"
       exit 1
    fi

fi

# Keep configure
touch ${DOMAIN_HOME}/.keep_conf

# Remove lok files
# find ${DOMAIN_HOME} -name "*.lok" -exec rm -f {} \;
# find ${DOMAIN_HOME} -name "*.DAT" -exec rm -f {} \;
# rm -rf ${DOMAIN_HOME}/servers/${ADMIN_NAME}/cache/*
# rm -rf ${DOMAIN_HOME}/servers/${ADMIN_NAME}/tmp/*

echo
echo "Apply Java Settings"
echo "=========================="

# Get USER_MEM_ARGS
USER_MEM_ARGS=$(_properties ${DOM_PROPERTIES_FILE} "Java" "java.user_mem_args")
if [ -z "${USER_MEM_ARGS}" ]; then
    echo "The USER_MEM_ARGS is blank. The USER_MEM_ARGS must be set in the properties file."
    exit 1
fi

# Get JAVA_OPTIONS
JAVA_OPTIONS=$(_properties ${DOM_PROPERTIES_FILE} "Java" "java.java_options")
if [ -z "${JAVA_OPTIONS}" ]; then
    echo "The JAVA_OPTIONS is blank. The JAVA_OPTIONS must be set in the properties file."
    exit 1
fi

# Set JAVA OPTIONS
export USER_MEM_ARGS=${USER_MEM_ARGS}
export JAVA_OPTIONS=${JAVA_OPTIONS}
echo "User Mem Args:   ${USER_MEM_ARGS}"
echo "Java Options:    ${JAVA_OPTIONS}"

${DOMAIN_HOME}/bin/setDomainEnv.sh

echo
echo "Starting the Admin Server"
echo "=========================="

# Start Admin Server and tail the logs

if [ "${DERBY_ENABLED}" == "true" ]; then
    ${DOMAIN_HOME}/startWebLogic.sh &
else
    ${DOMAIN_HOME}/startWebLogic.sh noderby & # runWLS without derby server
fi

# touch ${DOMAIN_HOME}/servers/${ADMIN_NAME}/logs/${ADMIN_NAME}.log
# tail -f ${DOMAIN_HOME}/servers/${ADMIN_NAME}/logs/${ADMIN_NAME}.log &

childPID=$!
wait $childPID

