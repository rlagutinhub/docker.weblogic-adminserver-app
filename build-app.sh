#!/bin/sh

# apt install openjdk-11-jdk-headless # jar

scriptDir="$( cd "$(dirname $0)" && pwd)"
if [ ! -d ${scriptDir} ]; then
    echo "Unable to determine the source directory where the application is found"
    echo "Using shell /bin/sh to determine and found ${scriptDir}"
    exit 1
fi

mkdir -p ${scriptDir}/files
rm -f ${scriptDir}/files/hello.*
jar -cvf ${scriptDir}/files/hello.war -C ${scriptDir}/source .
jar -cvf ${scriptDir}/files/hello.zip  -C ${scriptDir}/files/ hello.war
