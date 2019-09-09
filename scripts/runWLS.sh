#!/bin/bash

# NAME:   RUNWLS.SH
# DESC:   RUN WLS
# DATE:   28-08-2019
# LANG:   BASH
# AUTHOR: LAGUTIN R.A.
# EMAIL:  RLAGUTIN@MTA4.RU

########### SIGTERM handler ############
function _term() {

   echo "Stopping container."
   echo "SIGTERM received, shutting down the server!"
   # ${DOMAIN_HOME}/bin/stopWebLogic.sh

   # Shutdown domain
   # wlst.sh -skipWLSModuleScanning \
   #  -loadProperties ${DOMAIN_PROPERTIES_FILE} \
   #  -loadProperties ${SEC_PROPERTIES_FILE} \
   #  ${SCRIPTS_DIR}/shutdown-wls-domain.py

   # Shutdown domain (connect t3 or t3s with DemoTrust cert allow)
   source ${DOMAIN_HOME}/bin/setDomainEnv.sh
   java \
    -Dweblogic.security.SSL.ignoreHostnameVerification=true \
    -Dweblogic.security.CustomTrustKeyStoreType="JKS" \
    -Dweblogic.security.TrustKeyStore=CustomTrust \
    -Dweblogic.security.CustomTrustKeyStoreFileName="${ORACLE_HOME}/wlserver/server/lib/DemoTrust.jks" \
    weblogic.WLST \
    -skipWLSModuleScanning \
    -loadProperties ${DOMAIN_PROPERTIES_FILE} \
    -loadProperties ${SEC_PROPERTIES_FILE} \
    ${SCRIPTS_DIR}/shutdown-wls-domain.py

   retval=$?

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

# Get DOMAIN_PROPERTIES_FILE
DOMAIN_PROPERTIES_FILE=${PROPERTIES_DIR}/domain_base.properties
echo $DOMAIN_PROPERTIES_FILE
if [ ! -e "${DOMAIN_PROPERTIES_FILE}" ]; then
    echo "A Domain properties file needs to be supplied."
    exit 1
fi

# Get SEC_PROPERTIES_FILE
SEC_PROPERTIES_FILE=${PROPERTIES_DIR}/domain_security.properties
echo $SEC_PROPERTIES_FILE
if [ ! -e "${SEC_PROPERTIES_FILE}" ]; then
    echo "A properties file with the username and password needs to be supplied."
    exit 1
fi

# Get MOD_PROPERTIES_FILE
MOD_PROPERTIES_FILE=${PROPERTIES_DIR}/domain_modify.properties
echo $MOD_PROPERTIES_FILE
if [ ! -e "${MOD_PROPERTIES_FILE}" ]; then
    echo "A Domain modify properties file needs to be supplied."
    exit 1
fi

# Get APP_PROPERTIES_FILE
APP_PROPERTIES_FILE=${PROPERTIES_DIR}/domain_app.properties
echo $APP_PROPERTIES_FILE
if [ ! -e "${APP_PROPERTIES_FILE}" ]; then
    echo "A Domain app properties file needs to be supplied."
    exit 1
fi

# Get JAVA_PROPERTIES_FILE
JAVA_PROPERTIES_FILE=${PROPERTIES_DIR}/domain_java.properties
echo $JAVA_PROPERTIES_FILE
if [ ! -e "${JAVA_PROPERTIES_FILE}" ]; then
    echo "A java properties file needs to be supplied."
    exit 1
fi

# Get DOMAIN_NAME
DOMAIN_NAME=`cat ${DOMAIN_PROPERTIES_FILE} | grep "^DOMAIN_NAME" | cut -d "=" -f2-`
if [ -z "${DOMAIN_NAME}" ]; then
    echo "The DOMAIN_NAME is blank. The DOMAIN_NAME must be set in the properties file."
    exit 1
fi

# Get ADMIN_NAME
ADMIN_NAME=`cat ${DOMAIN_PROPERTIES_FILE} | grep "^ADMIN_NAME" | cut -d "=" -f2-`
if [ -z "${ADMIN_NAME}" ]; then
    echo "The ADMIN_NAME is blank. The ADMIN_NAME must be set in the properties file."
    exit 1
fi

# Get USERNAME
USER=`cat ${SEC_PROPERTIES_FILE} | grep "^username" | cut -d "=" -f2-`
if [ -z "${USER}" ]; then
    echo "The domain username is blank. The Admin username must be set in the properties file."
    exit 1
fi

# Get PASSWORD
PASS=`cat ${SEC_PROPERTIES_FILE} | grep "^password" | cut -d "=" -f2-`
if [ -z "${PASS}" ]; then
    echo "The domain password is blank.  The Admin password must be set in the properties file."
    exit 1
fi

echo
echo "Domain HOME"
echo "=========================="

#Define DOMAIN_HOME
export DOMAIN_HOME=${ORACLE_HOME}/user_projects/domains/${DOMAIN_NAME}
echo "Domain Home is: " $DOMAIN_HOME

echo
echo "Docker Container ID"
echo "=========================="

#Define Container ID
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
    echo "Domain already configured is: " $DOMAIN_NAME
fi

if [ $ADD_DOMAIN -eq 0 ]; then

    # Create domain
    wlst.sh -skipWLSModuleScanning \
     -loadProperties ${DOMAIN_PROPERTIES_FILE} \
     -loadProperties ${SEC_PROPERTIES_FILE} \
     ${SCRIPTS_DIR}/create-wls-domain.py

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
    # /bin/bash; exit 0 # troubleshooting

    # Create Logs folder
    # mkdir -p ${DOMAIN_HOME}/logs/
    mkdir -p ${ORACLE_HOME}/logs/

    # Modify domain
    wlst.sh -skipWLSModuleScanning \
     -loadProperties ${DOMAIN_PROPERTIES_FILE} \
     -loadProperties ${SEC_PROPERTIES_FILE} \
     ${SCRIPTS_DIR}/modify-wls-domain.py -p ${MOD_PROPERTIES_FILE} -c ${CID}

    retval=$?

    echo  "RetVal from Domain modify $retval"

    if [ $retval -ne 0 ]; then
       echo "Domain Modify Failed.. Please check the Domain Logs"
       exit 1
    fi

    # Create datasource
    # wlst.sh -skipWLSModuleScanning \
     # -loadProperties ${DOMAIN_PROPERTIES_FILE} \
     # -loadProperties ${SEC_PROPERTIES_FILE} \
     # ${SCRIPTS_DIR}/datasource-wls-domain.py

    # retval=$?

    # echo  "RetVal from Domain modify $retval"

    # if [ $retval -ne 0 ]; then
       # echo "Datasource Creation Failed.. Please check the Domain Logs"
       # exit
    # fi

    # Deploy app
    wlst.sh -skipWLSModuleScanning \
     -loadProperties ${DOMAIN_PROPERTIES_FILE} \
     -loadProperties ${SEC_PROPERTIES_FILE} \
     ${SCRIPTS_DIR}/app-wls-domain.py -p ${APP_PROPERTIES_FILE} -m offline # offline or online

    retval=$?

    echo  "RetVal from Domain modify $retval"

    if [ $retval -ne 0 ]; then
       echo "App Deploy Failed.. Please check the Domain Logs"
       exit 1
    fi

fi

# Keep configure
touch ${DOMAIN_HOME}/.keep_conf

# Remove lok files
find ${DOMAIN_HOME} -name "*.lok" -exec rm -f {} \;
find ${DOMAIN_HOME} -name "*.DAT" -exec rm -f {} \;
rm -rf ${DOMAIN_HOME}/servers/${ADMIN_NAME}/cache/*
rm -rf ${DOMAIN_HOME}/servers/${ADMIN_NAME}/tmp/*
# /bin/bash; exit 0 # troubleshooting

echo
echo "Apply Java Settings"
echo "=========================="

# Get USER_MEM_ARGS
USER_MEM_ARGS=`cat ${JAVA_PROPERTIES_FILE} | grep "^USER_MEM_ARGS" | cut -d "=" -f2-`
if [ -z "${USER_MEM_ARGS}" ]; then
    echo "The USER_MEM_ARGS is blank. The USER_MEM_ARGS must be set in the properties file."
    exit 1
fi

# Get JAVA_OPTIONS
JAVA_OPTIONS=`cat ${JAVA_PROPERTIES_FILE} | grep "^JAVA_OPTIONS" | cut -d "=" -f2-`
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
# ${DOMAIN_HOME}/startWebLogic.sh
${DOMAIN_HOME}/startWebLogic.sh noderby & # runWLS without derby server

# touch ${DOMAIN_HOME}/servers/${ADMIN_NAME}/logs/${ADMIN_NAME}.log
# tail -f ${DOMAIN_HOME}/servers/${ADMIN_NAME}/logs/${ADMIN_NAME}.log &

childPID=$!
wait $childPID

