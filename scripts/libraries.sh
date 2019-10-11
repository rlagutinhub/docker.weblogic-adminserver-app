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

        if [ "$(echo "$SECTION" | sed 's/ *$//g')" == '['$SECTION_F']' ]; then

            SAVEIFS=$IFS; IFS='='

            while read KEY VALUE; do

                if [ "$(echo "$KEY" | sed 's/ *$//g')" == "$KEY_F" ]; then

                    echo $VALUE | sed 's/ *$//g'
                    break

                fi

            done

            IFS=$SAVEIFS

        fi

    done < $FILE_F

}
