#!/bin/bash
# encode or decode base64 multiple times
case $1 in 
    encode )
        if [[ ${3} == "-i" ]]; then
            flagz=$( cat ${4} )
        else
            flagz="${3}"
        fi
        for i in `seq 1 ${2}`; do
            flagz=$( echo "${flagz}" | base64 )
        done
        echo "${flagz}"
        ;;
    decode )
        if [[ ${3} == "-i" ]]; then
            flagz=$( cat ${4} )
        else
            flagz="${3}"
        fi
        for i in `seq 1 ${2}`; do
            flagz=$( echo "${flagz}" | base64 -D)
        done
        echo "${flagz}"
        ;;
    *) echo "Invalid option  -- takes 'encode' or 'decode' as first arg"; exit;;
esac
if [[ $4 == "-o" ]]; then
    echo "${flagz}" >>${5}
elif [[ $5 == "-o" ]]; then
    echo "${flagz}" >>${6}
fi
