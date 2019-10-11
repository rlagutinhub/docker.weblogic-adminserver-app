#!/bin/bash

# $1 - $FILE_F
# $2 - $SECTION_F
# $3 - $KEY_F
function _properties() {

    local FILE_F=$1
    local SECTION_F=$2
    local KEY_F=$3

    if [ ! -r "$FILE_F" ]; then exit 1; fi

    while read SECTION; do

        SECTION=$(echo "$SECTION" | sed 's/ *$//g')

        if [ "$SECTION" == '['$SECTION_F']' ]; then    

            SAVEIFS=$IFS; IFS='='

            while read KEY VALUE; do

                KEY=$(echo "$KEY" | sed 's/ *$//g')

                if [ "${KEY:0:1}" == "[" ]; then break; fi

                if [ "$KEY" == "$KEY_F" ]; then

                    VALUE=$(echo $VALUE | sed 's/ *$//g')

                    echo $VALUE
                    break

                fi

            done

            IFS=$SAVEIFS

        fi

    done < $FILE_F

}
