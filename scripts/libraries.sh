#!/bin/bash

# NAME:   LIBRARIES.SH
# DESC:   LIBRARIES
# DATE:   14-10-2019
# LANG:   BASH
# AUTHOR: LAGUTIN R.A.
# EMAIL:  RLAGUTIN@MTA4.RU

# $1 - $FILE_F
# $2 - $SECTION_F
# $3 - $KEY_F
function get_ini() {

    local FILE_F=$1
    local SECTION_F=$2
    local KEY_F=$3

    if [ ! -r "$FILE_F" ]; then exit 1; fi

    while read SECTION; do

        SECTION=$(echo "$SECTION" | sed 's/ *$//g')

        if [ "$SECTION" == '['$SECTION_F']' ]; then

            while read PROPERTIES; do

                if [[ $PROPERTIES =~ ^\[.*\]$ ]]; then break; fi
                if [[ ! $(echo $PROPERTIES | grep "=") ]]; then continue; fi

                KEY=$(echo "$(echo $PROPERTIES | cut -d "=" -f 1)" | sed 's/ *$//g')
                VALUE=$(echo "$(echo $PROPERTIES | cut -d "=" -f 2-)" | sed 's/ *$//g')

                if [ "$KEY" == "$KEY_F" ]; then echo $VALUE; break; fi

           done

        fi

    done < $FILE_F

}
